# from time import sleep
from celery import shared_task

from blog_api.auth_app.functions.mail import password_updated_mail, reset_password_mail, user_registration_mail


@shared_task
def send_verify_account_html_mail(user):
    user_registration_mail(user)


@shared_task
def send_password_updated_html_mail(user):
    password_updated_mail(user)


@shared_task
def send_reset_password_mail(user):
    reset_password_mail(user)
