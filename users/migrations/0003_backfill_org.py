from django.db import migrations


def backfill_orgs(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Organization = apps.get_model('users', 'Organization')
    for user in User.objects.filter(org__isnull=True):
        name = user.institute_name or user.username
        org = Organization.objects.create(name=name)
        user.org = org
        user.save(update_fields=['org'])


def remove_backfill_orgs(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Organization = apps.get_model('users', 'Organization')
    org_ids = User.objects.values_list('org_id', flat=True).distinct()
    Organization.objects.filter(id__in=org_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_add_organization'),
    ]

    operations = [
        migrations.RunPython(backfill_orgs, remove_backfill_orgs),
    ]
