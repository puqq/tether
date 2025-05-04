# tether_main/signals.py
import json, random
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .models import Relationship

@receiver(post_save, sender=Relationship)
def sync_celery_schedule(sender, instance, created, **kwargs):
    name = f"reminder-{instance.pk}"

    # 1) On initial creation: just assign the random slot, then exit.
    if created:
        if instance.reminder_frequency == Relationship.WEEKLY:
            instance.weekly_day = random.randint(0, 6)
        elif instance.reminder_frequency == Relationship.MONTHLY:
            instance.monthly_day = random.randint(1, 28)
        # persist only those two fields
        instance.save(update_fields=['weekly_day', 'monthly_day'])
        return      # <-- important: don't build or create the task yet

    # 2) If user changed their frequency, re‑assign a new random slot and exit—
    #    the nested save will call us again without 'reminder_frequency' in update_fields.
    update_fields = kwargs.get('update_fields')
    if update_fields and 'reminder_frequency' in update_fields:
        if instance.reminder_frequency == Relationship.WEEKLY:
            instance.weekly_day = random.randint(0, 6)
            instance.monthly_day = None
        elif instance.reminder_frequency == Relationship.MONTHLY:
            instance.monthly_day = random.randint(1, 28)
            instance.weekly_day = None
        instance.save(update_fields=['weekly_day', 'monthly_day'])
        return

    # 3) From here on out (created=False, not a pure frequency change),
    #    we actually sync the PeriodicTask.
    #    First, delete any old one:
    PeriodicTask.objects.filter(name=name).delete()

    # 4) If they’ve paused reminders, we stop here
    if instance.paused:
        return

    # 5) Build the CrontabSchedule
    hour   = instance.time_of_day.hour
    minute = instance.time_of_day.minute
    freq   = instance.reminder_frequency

    if freq == Relationship.DAILY:
        sched, _ = CrontabSchedule.objects.get_or_create(hour=hour, minute=minute)
    elif freq == Relationship.WEEKLY:
        sched, _ = CrontabSchedule.objects.get_or_create(
            day_of_week=str(instance.weekly_day),
            hour=hour, minute=minute
        )
    else:  # MONTHLY
        sched, _ = CrontabSchedule.objects.get_or_create(
            day_of_month=str(instance.monthly_day),
            hour=hour, minute=minute
        )

    # 6) Finally, create the PeriodicTask once
    PeriodicTask.objects.create(
        name    = name,
        task    = 'tether_main.tasks.send_reminder_email',
        crontab = sched,
        args    = json.dumps([instance.pk]),
    )
@receiver(post_delete, sender=Relationship)
def remove_schedule(sender, instance, **kwargs):
    # clean up when a Relationship is deleted
    PeriodicTask.objects.filter(name=f"reminder-{instance.pk}").delete()