import glob
import os

from flask import url_for
from flask_mail import  Message

from VM_proj_flask import User, mail

def cleanup_temp_folder():
    # Define the path to the temporary folder
    temp_folder_path = os.path.join("static", "temp")

    # Remove old files in the temporary folder
    for file_path in glob.glob(os.path.join(temp_folder_path, "*.png")):
        os.remove(file_path)


def send_mail(user: User):
    token = user.get_token()
    msg = Message(
        subject="VM Project Password Reset",
        recipients=[user.email],
        sender="vmproj@outlook.com",
    )
    msg.body = f"""To reset your password, follow the link below.
{url_for('forgot_password_token', token=token, _external=True)}

This link is valid for 10 minutes.

If you did not request a password reset, ignore this email.

"""
    mail.send(msg)
