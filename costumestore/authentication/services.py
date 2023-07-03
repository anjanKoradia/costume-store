from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(name, email, email_token):
    """
    Sends an account activation email to the specified user.

    This function constructs an email message with an activation link
    and sends it to the user's email address.

    Args:
        name (str): The name of the user.
        email (str): The email address of the user.
        email_token (str): The activation token for the user's account.

    Returns:
        None
    """
    subject = "Costumer Store Account Activation"
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi {name.capitalize()}, Click on the link to activate your " \
              f"account http://127.0.0.1:8000/auth/activate/{email_token}"

    send_mail(subject, message, email_from, [email], fail_silently=False)
