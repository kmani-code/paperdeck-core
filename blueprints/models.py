from django.db import models
from django.conf import settings


class Blueprint(models.Model):
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blueprints')
    name       = models.CharField(max_length=300)
    exam       = models.CharField(max_length=100)
    duration   = models.CharField(max_length=50)
    total_marks = models.IntegerField(default=0)
    neg_marking = models.CharField(max_length=100, default='')
    sections   = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pd_blueprints'
        ordering = ['-created_at']
