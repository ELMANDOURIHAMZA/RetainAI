from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db, Tenant
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Cet email est déjà utilisé.', 'error')
            return redirect(url_for('auth.register'))
            
        # Create Tenant
        tenant = Tenant(name=company_name)
        db.session.add(tenant)
        db.session.flush()
        
        # Create User
        new_user = User(
            email=email,
            name=name,
            tenant_id=tenant.id,
            role='admin'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('dashboard.index'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate token
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(email, salt='password-reset-salt')
            
            # Mock Email Sending
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            print(f"\n[MOCK EMAIL] To: {email}")
            print(f"[MOCK EMAIL] Subject: Réinitialisation de mot de passe")
            print(f"[MOCK EMAIL] Link: {reset_link}\n")
            
            flash('Si cet email existe, un lien de réinitialisation a été envoyé.', 'info')
            return redirect(url_for('auth.login'))
        else:
             flash('Si cet email existe, un lien de réinitialisation a été envoyé.', 'info')
             return redirect(url_for('auth.login'))
             
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('Le lien de réinitialisation est invalide ou expiré.', 'error')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return redirect(url_for('auth.reset_password', token=token))
            
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            db.session.commit()
            flash('Votre mot de passe a été mis à jour. Vous pouvez vous connecter.', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/reset_password.html', token=token)
