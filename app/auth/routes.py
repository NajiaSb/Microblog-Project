from flask import render_template, redirect, url_for, flash, request, session
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
import base64


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


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.mfa_secret_key = pyotp.random_base32()  # generating a new secret key
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))

        mfa_required(user)

        if user.mfa_enabled is not None:
            return redirect(url_for('auth.mfa'))
        else:
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)


def mfa_required(user):
    if user.mfa_secret_key is not None:
        session['mfa_required'] = True
    else:
        session.pop('mfa_required', None)


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
def mfa():
    if not session.get('mfa_required', False):
        return redirect(url_for('main.index'))

    form = MFAForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            # User is registering for the first time
            user = User.query.filter_by(email=session['user_email']).first()
            if user and pyotp.TOTP(user.mfa_secret_key).verify(form.mfa_token.data):
                user.mfa_enabled = form.remember_me.data
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                session.pop('user_email', None)
                session.pop('mfa_required', None)
                flash('You have successfully enabled MFA.')
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('Invalid MFA token.')
                return redirect(url_for('auth.mfa'))
        else:
            # User has logged in before and has an MFA key
            user_secret = current_user.get_mfa_secret()
            totp = pyotp.TOTP(user_secret)
            if totp.verify(form.mfa_token.data):
                current_user.mfa_enabled = form.remember_me.data
                db.session.commit()
                session.pop('mfa_required', None)
                flash('You have successfully enabled MFA.')
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('Invalid MFA token.')
                return redirect(url_for('auth.mfa'))

    if current_user.is_anonymous:
        user_email = session.get('user_email')
        if not user_email:
            flash('You need to fill out your registration form first')
            return redirect(url_for('auth.register'))
        else:
            qr_code = pyotp.totp.TOTP(pyotp.random_base32()).provisioning_uri(user_email)
            img = qrcode.make(qr_code)
            buffered = BytesIO()
            img.save(buffered, format="png")
            qr_image_data = buffered.getvalue()
            return render_template('auth/mfa.html', title='Two-Factor Authentication', form=form, qr_image_data=base64.b64encode(qr_image_data))
    else:
        # User has logged in before and has an MFA key
        user_secret = current_user.get_mfa_secret()
        totp = pyotp.TOTP(user_secret)
        qr_code = totp.provisioning_uri(current_user.email)
        img = qrcode.make(qr_code)
        buffered = BytesIO()
        img.save(buffered, format="png")
        qr_image_data = buffered.getvalue()
        return render_template('auth/mfa.html', title='Two-Factor Authentication', form=form, qr_image_data=base64.b64encode(qr_image_data))
