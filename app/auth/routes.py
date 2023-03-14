import pyqrcode
from flask import render_template, redirect, url_for, flash, request, session, app, abort
from flask_mail import Message
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
from app import db, mail
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email
import pyotp
import qrcode
from io import BytesIO
import bcrypt


@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data) or \
                not user.verify_totp(form.token.data):
            flash('Invalid username, password or token.')
            return redirect(url_for('auth.login'))

        # log user in
        login_user(user)
        flash('You are now logged in!')
        return redirect(url_for('auth.index'))
    return render_template('auth/login.html', title=_('Log In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        # add new user to the database
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # redirect to the two-factor auth page, passing username in session
        session['username'] = user.username
        return redirect(url_for('auth.two_factor_setup'))
    return render_template('auth/register.html', title=_('Register'), form=form)


@bp.route('/twofactor', methods=['GET', 'POST'])
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('auth.index'))
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('auth/two-factor-setup.html', title=_('Two Factor')), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@bp.route('/qrcode', methods=['GET', 'POST'])
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # generate a token for the password reset link
            token = user.get_reset_password_token()

            # output the reset link to std_out
            print(
                f'To reset your password, click on the following link: {url_for("auth.reset_password", token=token,_external=True)}')

            flash(_('Console Output has your reset link!'))
        else:
            flash(_('Invalid email address'))
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
        if not user.verify_password(form.password.data):
            user.password = form.password.data
            db.session.commit()
            flash(_('Your password has been reset.'))    #compare hash and if pass is diff reset it 
        else:
            flash(_('Your new password cannot be the same as your old password.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


