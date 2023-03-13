from flask import render_template, redirect, url_for, flash, request, session, app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, MFAForm
from app.models import User
from app.auth.email import send_password_reset_email
import pyotp
import qrcode
from io import BytesIO
import bcrypt


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        session['mfa_required'] = True  # Set MFA flag in session
        return redirect('auth.mfa')
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


def mfa_setup(email):
    # Generate a new random secret key
    secret_key = pyotp.random_base32()

    # Generate a new QR code for the secret key
    qr_code = qrcode.make(pyotp.totp.TOTP(secret_key).provisioning_uri(email))

    # Create an MFA form with the email and secret key
    form = MFAForm(email=email, secret_key=secret_key)

    # Return the form and QR code as a tuple
    return form, qr_code


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Set up MFA for the user
        mfa_form, mfa_qr_code = mfa_setup(user.email)

        # Save the MFA secret key to the user's record in the database
        user.mfa_secret_key = mfa_form.secret_key.data
        db.session.commit()

        # Render the MFA setup page
        return render_template('auth/mfa_setup.html', title=_('MFA Setup'), qr_code=mfa_qr_code, form=mfa_form)

    return render_template('auth/register.html', title=_('Register'), form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/mfa', methods=['GET', 'POST'])
@login_required
def mfa():
    form = MFAForm()
    if form.validate_on_submit():
        # Verify the MFA token entered by the user
        totp = pyotp.TOTP(current_user.mfa_secret_key)
        if totp.verify(form.mfa_token.data):
            # Set the remember_me cookie if the user checked the box
            remember_me = form.remember_me.data
            session.permanent = remember_me
            app.logger.info(f"User {current_user.username} logged in with MFA.")

            return redirect(request.args.get('next') or url_for('main.index'))

        flash(_('Invalid MFA token'))

    # Set the value of the secret_key field in the form
    form.secret_key.data = current_user.mfa_secret_key

    return render_template('auth/mfa.html', title=_('MFA'), form=form)

