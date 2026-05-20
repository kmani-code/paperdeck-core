import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework.decorators import api_view

from blueprints.processor.blueprintprocessor import blueprint_req_schema
from blueprints.service.blueprintservice import BlueprintService
from utility.decorator.auth import auth_required
from utility.utilityobj import ErrorResponse


@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@auth_required
@transaction.atomic
def blueprint(request):
    if request.method == 'GET':
        return _fetch(request)
    elif request.method == 'POST':
        return _post(request)
    elif request.method == 'DELETE':
        return _delete(request)


def _fetch(request):
    scope = request.scope
    org_id = scope.get('org_id')
    blueprint_id = request.query_params.get('blueprint_id')
    service = BlueprintService(scope)
    if blueprint_id:
        resp = service.fetch_one(blueprint_id, scope['user_id'], org_id=org_id)
        if isinstance(resp, ErrorResponse):
            return HttpResponse(resp.to_json(), status=resp.status, content_type='application/json')
        return HttpResponse(resp.to_json(), content_type='application/json')
    resp_list = service.fetch_all(scope['user_id'], org_id=org_id)
    return HttpResponse(json.dumps([b.to_dict() for b in resp_list]), content_type='application/json')


def _post(request):
    scope = request.scope
    org_id = scope.get('org_id')
    obj = blueprint_req_schema.load(request.data)
    service = BlueprintService(scope)
    resp = service.create_or_update(obj, scope['user_id'], org_id=org_id)
    if isinstance(resp, ErrorResponse):
        return HttpResponse(resp.to_json(), status=resp.status, content_type='application/json')
    return HttpResponse(resp.to_json(), content_type='application/json')


def _delete(request):
    scope = request.scope
    org_id = scope.get('org_id')
    blueprint_id = request.query_params.get('blueprint_id')
    if not blueprint_id:
        return HttpResponse(
            ErrorResponse(status=400, message='blueprint_id is required').to_json(),
            status=400, content_type='application/json'
        )
    service = BlueprintService(scope)
    resp = service.delete(blueprint_id, scope['user_id'], org_id=org_id)
    if isinstance(resp, ErrorResponse):
        return HttpResponse(resp.to_json(), status=resp.status, content_type='application/json')
    return HttpResponse(resp.to_json(), content_type='application/json')
