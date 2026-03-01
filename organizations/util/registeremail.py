from django.core.mail import send_mail
from django.conf import settings


def send_org_request_status_mail(req):

    if req.status == "APPROVED":
        subject = f"{req.org_name} Registration Approved"

        message = f"""
Dear {req.admin_name},

We are pleased to inform you that your organization registration request
for "{req.org_name}" has been successfully APPROVED.

Your organization account has now been created.

You can log in using your registered email address:
{req.admin_email}

If you have not yet set your password, please use the password reset option.

We look forward to working with you.

Best regards,
HR Management System Team
"""

    elif req.status == "REJECTED":
        subject = f"{req.org_name} Registration Update"

        message = f"""
Dear {req.admin_name},

Thank you for your interest in registering "{req.org_name}" with our system.

After reviewing your application, we regret to inform you that your
organization request has been REJECTED.

Reason for rejection:
{req.rejection_reason if req.rejection_reason else "Not specified"}

You may correct the details and apply again, or contact our support team
for assistance.

Best regards,
HR Management System Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [req.admin_email,req.org_email],
    )