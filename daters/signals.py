from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from dayofthedate import settings
from .models import DaterUser


@receiver(m2m_changed, sender=DaterUser.match.through)
def match_updated(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add" and not reverse:
        for pk in pk_set:
            matched_user = DaterUser.objects.get(pk=pk)
            if matched_user.match.filter(id=instance.id).exists():
                send_mail(
                    subject='Взаимная симпатия',
                    message=f"Вы понравились пользователю {instance.username}! Email участника: {instance.email}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[matched_user.email],
                )
                send_mail(
                    subject='Взаимная симпатия',
                    message=f"Вы понравились пользователю {matched_user.username}! Email участника: {matched_user.email}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[instance.email],
                )
