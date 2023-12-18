import re  # Import the regular expression module

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length, ValidationError

from VM_proj_flask.models.user import User
from VM_proj_flask.cnn_model.MNSIT_CNN_util import *

def validate_password(password):
    # Check for allowed characters in the password
    if not re.match(r'^[a-zA-Z0-9!@#$%^&*_+:;,.?/~\\-]+$', password.data):
        raise ValidationError(
            "Password contains invalid characters. Please use only letters, numbers, and allowed symbols."
        )

    # Check for security risks (you can customize this based on your requirements)
    common_passwords = ["password", "123456", "qwerty"]
    if password.data.lower() in common_passwords:
        raise ValidationError(
            "Please choose a more secure password. Avoid common choices."
        )


class RegisterForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Email(), Length(min=4, max=254)],
        render_kw={"placeholder": "Email"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Register")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                "That email already exists. Please choose a different one."
            )
        
    def validate_password(self, password):
        validate_password(password)




class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Email(), Length(min=4, max=254)],
        render_kw={"placeholder": "Email"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Email(), Length(min=4, max=254)],
        render_kw={"placeholder": "Email"},
    )

    submit = SubmitField("Send verification email")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    confirm_password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Confirm Password"},
    )

    def validate_password(self, password):
        validate_password(password)
    
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError(
                "Passwords in both fields have to match!"
            )


    submit = SubmitField("Update Password")
