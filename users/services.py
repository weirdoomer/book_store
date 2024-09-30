from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.urls import reverse


def send_verification_email(object):
    link = reverse(
        "users:email_verification",
        kwargs={"code": object.code},
    )

    if settings.DEBUG:
        verification_link = f"http://{settings.DOMAIN_NAME}{link}"
    else:
        verification_link = (
            f"https://{Site.objects.get_current().domain}{link}"
        )

    subject = f"Подтверждение учетной записи для {object.user.username}"
    message = "Для подтверждения учетной записи для {} перейдите по ссылке: {}".format(
        object.user.email, verification_link
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[object.user.email],
        fail_silently=False,
    )
