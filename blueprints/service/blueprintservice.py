from blueprints.models import Blueprint
from blueprints.processor.blueprintprocessor import BlueprintResponse
from utility.dbservice import DBService
from utility.utilityobj import ErrorResponse, SuccessResponse


def _build(b: Blueprint) -> BlueprintResponse:
    return BlueprintResponse(
        id=b.id,
        name=b.name,
        exam=b.exam,
        duration=b.duration,
        total_marks=b.total_marks,
        neg_marking=b.neg_marking,
        sections=b.sections or [],
        created_at=b.created_at.isoformat(),
    )


class BlueprintService(DBService):
    def __init__(self, scope):
        super().__init__(scope)

    def fetch_all(self, user_id, org_id=None):
        qs = Blueprint.objects.filter(owner__org_id=org_id) if org_id else Blueprint.objects.filter(owner_id=user_id)
        return [_build(b) for b in qs]

    def fetch_one(self, blueprint_id, user_id, org_id=None):
        try:
            if org_id:
                return _build(Blueprint.objects.get(id=blueprint_id, owner__org_id=org_id))
            return _build(Blueprint.objects.get(id=blueprint_id, owner_id=user_id))
        except Blueprint.DoesNotExist:
            return ErrorResponse(status=404, message='Blueprint not found')

    def create_or_update(self, req, user_id, org_id=None):
        if req.id is None:
            b = Blueprint.objects.create(
                owner_id=user_id,
                name=req.name,
                exam=req.exam,
                duration=req.duration,
                total_marks=req.total_marks,
                neg_marking=req.neg_marking,
                sections=req.sections,
            )
        else:
            try:
                if org_id:
                    b = Blueprint.objects.get(id=req.id, owner__org_id=org_id)
                else:
                    b = Blueprint.objects.get(id=req.id, owner_id=user_id)
            except Blueprint.DoesNotExist:
                return ErrorResponse(status=404, message='Blueprint not found')
            b.name = req.name
            b.exam = req.exam
            b.duration = req.duration
            b.total_marks = req.total_marks
            b.neg_marking = req.neg_marking
            b.sections = req.sections
            b.save()
        return _build(b)

    def delete(self, blueprint_id, user_id, org_id=None):
        if org_id:
            deleted, _ = Blueprint.objects.filter(id=blueprint_id, owner__org_id=org_id).delete()
        else:
            deleted, _ = Blueprint.objects.filter(id=blueprint_id, owner_id=user_id).delete()
        if not deleted:
            return ErrorResponse(status=404, message='Blueprint not found')
        return SuccessResponse(status=200, message='Blueprint deleted')
