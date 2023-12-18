import os
import uuid

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from VM_proj_flask.cnn_model.MNSIT_CNN_util import *
from VM_proj_flask.common import cleanup_temp_folder, send_mail
from VM_proj_flask.forms import *
from VM_proj_flask.main import bp

from VM_proj_flask.extensions import bycript, db, login_manager, mail

model = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route("/")
def home():
    return render_template("/home.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bycript.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect("dashboard")

        error = "Email or password are incorrect."
    return render_template("auth/login.html", form=form, error=error)


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash("Reset request sent. Check your mail", "success")
            return redirect(url_for("main.forgot_password"))
        else:
            error = "Incorrect email given."

    return render_template("auth/forgot_password.html", form=form, error=error)


@bp.route("/forgot_password/<token>", methods=["GET", "POST"])
def forgot_password_token(token):
    user = User.verify_token(token)
    if user is None:
        flash(
            "The reset password token is invalid or expired. Please try again",
            "warning",
        )
        return redirect(url_for("main.forgot_password"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bycript.generate_password_hash(password=form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Password updated!", "success")
        return redirect(url_for("main.login"))

    return render_template("auth/reset_password.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bycript.generate_password_hash(password=form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.login"))
    return render_template("auth/register.html", form=form)


@bp.route("/dashboard")
@login_required
def dashboard():
    # Access the parameters passed in the URL
    image_url = request.args.get("image_url")
    result = request.args.get("result")

    # Render the result page with the parameters
    return render_template("dashboard.html", image_url=image_url, result=result)


@login_required
@bp.route("/upload", methods=["POST"])
def upload():
    # Cleanup temporary folder when the page is reloaded
    cleanup_temp_folder()

    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return render_template("dashboard.html", image_url=None, result=None)

    # Load and preprocess the image
    start_img, formatted_img = load_image_from_file(file)

    # Make predictions using the loaded Keras model
    result = model.predict(image=formatted_img)

    if result == "error":
        return render_template("dashboard.html", image_url=None, result=result)

    # Save the image temporarily for display
    unique_filename = f"{uuid.uuid4()}.png"
    temp_image_path = os.path.join("static", "temp", unique_filename)
    start_img.save(temp_image_path)

    # Provide the relative URL to the template
    image_url = f"/static/temp/{unique_filename}"
    return redirect(url_for("main.dashboard", image_url=image_url, result=result))
