import requests
from decouple import config, UndefinedValueError
from django.conf import settings
from python_http_client import BadRequestsError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Personalization
from django.core.mail import send_mail as django_send_mail


def get_azure_connection_dict():
    key_list = [
        'AD_app_id',
        'AD_app_secret',
        'AD_redirect',
        'AD_authority',
        'AD_authorize_endpoint',
        'AD_token_endpoint',
    ]
    my_dict = dict()
    for key in key_list:
        casting = str
        my_dict[key] = config(key, cast=casting, default="")
    return my_dict


def azure_ad_values_exist(connection_dict):
    key_list = [
        'AD_app_id',
        'AD_app_secret',
        'AD_redirect',
        'AD_authority',
        'AD_authorize_endpoint',
        'AD_token_endpoint',
    ]
    # if all values are present, below expression should be evaluated as False
    there_is_something_missing = False in [connection_dict[key] != "" for key in key_list]
    return there_is_something_missing is False


def db_connection_values_exist(connection_dict):
    key_list = [
        # 'DB_MODE',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
    # if all values are present, below expression should be evaluated as False
    there_is_something_missing = False in [connection_dict[key] != "" for key in key_list]
    return there_is_something_missing is False


def get_db_connection_dict():
    key_list = [
        'DB_MODE',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
    my_dict = dict()
    for key in key_list:
        casting = int if "port" in key.lower() else str
        my_dict[key] = config(key, cast=casting, default="")
    return my_dict



def custom_send_mail(subject, html_message, from_email, recipient_list):
    """
    The role of this function is to handle the sending of an email message based on the configuration of the project setting.py file.
    - If settings.USE_SENDGRID = True, the mail will be sent with the python sendgrid package using the sendgrid REST api
    - If settings.USE_SMTP_EMAIL = True, the email will be send with django's send_mail function.
    - If settings.USE_SMTP_EMAIL and settings.USE_SENDGRID are both false, no email will be sent.

    :param subject:
    :param html_message:
    :param from_email:
    :param recipient_list:
    :return:
    """

    if settings.USE_SENDGRID:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        from_email = Email(from_email)
        to_list = Personalization()
        for email in set(recipient_list):
            to_list.add_to(Email(email))
        mail = Mail(
            from_email=from_email,
            to_emails=None,
            subject=subject,
            html_content=html_message
        )
        mail.add_personalization(to_list)
        try:
            sg.send(mail)
        except BadRequestsError:
            print("bad request. email not sent")

    elif settings.USE_SMTP_EMAIL:
        django_send_mail(
            message='',
            subject=subject,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )

    else:
        print('No email configuration present in application...')
        print("FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(from_email, recipient_list, subject, html_message))