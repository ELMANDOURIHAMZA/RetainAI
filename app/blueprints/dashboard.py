from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app, send_file
from flask_login import login_required, current_user
from app.models import Customer, Subscription, Prediction, db, Tenant, Notification, User
from app.services.ai_service import generate_churn_insight
from app.services.ml_service import train_model
import uuid
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from io import BytesIO
from werkzeug.utils import secure_filename

dashboard_bp = Blueprint('dashboard', __name__)

# --- Mock Data Generators ---
def generate_campaign_data():
    return [
        {'name': 'Rétention Hiver 2024', 'segment': 'Risque Élevé', 'channel': 'Email', 'status': 'Terminé', 'date': '2024-01-15', 'roi': '125%'},
        {'name': 'Promo Fibre', 'segment': 'ADSL Users', 'channel': 'SMS', 'status': 'En cours', 'date': '2024-02-01', 'roi': 'Pending'},
        {'name': 'Winback Q1', 'segment': 'Churned', 'channel': 'Email', 'status': 'Terminé', 'date': '2024-03-10', 'roi': '85%'},
        {'name': 'Upsell Streaming', 'segment': 'Actifs', 'channel': 'App', 'status': 'Planifié', 'date': '2024-04-05', 'roi': '-'},
        {'name': 'Enquête Satisfaction', 'segment': 'Nouveaux', 'channel': 'Email', 'status': 'En cours', 'date': '2024-03-28', 'roi': 'N/A'}
    ]

def generate_survival_data():
    # Mock Kaplan-Meier data
    months = list(range(0, 73))
    # Curve 1: Fiber
    prob_fiber = [100]
    for i in range(1, 73):
        drop = 0.5 if i < 12 else (1.2 if i < 24 else 0.3)
        prob_fiber.append(max(0, prob_fiber[-1] - drop))
    
    # Curve 2: ADSL
    prob_adsl = [100]
    for i in range(1, 73):
        drop = 0.8 if i < 12 else (0.5 if i < 24 else 0.2)
        prob_adsl.append(max(0, prob_adsl[-1] - drop))
        
    return {'months': months, 'fiber': prob_fiber, 'adsl': prob_adsl}

def generate_mlops_data():
    import random
    months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    accuracy = [88, 87, 89, 86, 82, 78] # Dropping trend
    
    # Drift Histograms
    dist_train = [random.gauss(50, 15) for _ in range(500)]
    dist_current = [random.gauss(65, 20) for _ in range(500)] # Shifted
    
    return {'months': months, 'accuracy': accuracy, 'dist_train': dist_train, 'dist_current': dist_current}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dashboard_bp.context_processor
def inject_user():
    return dict(current_user=current_user)

@dashboard_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    filter_status = request.args.get('status', 'all')
    per_page = 5
    
    query = Customer.query.join(Subscription)
    
    if filter_status == 'churned':
        query = query.filter(Customer.churn_label == True)
    elif filter_status == 'active':
        query = query.filter(Customer.churn_label == False)
        
    pagination = query.order_by(Customer.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    total = Customer.query.count()
    churned = Customer.query.filter_by(churn_label=True).count()
    churn_rate = (churned / total * 100) if total > 0 else 0
    
    return render_template('dashboard/index.html', 
                           pagination=pagination,
                           filter_status=filter_status,
                           kpis={
                               'total': total,
                               'risk': churned,
                               'avg_risk': round(churn_rate, 1)
                           })

def get_filtered_customers_query(status='all', persona='all', search_id='', search_global=''):
    query = Customer.query.join(Subscription)
    
    if search_global:
        query = query.filter(Customer.external_id.ilike(f'%{search_global}%'))
        
    if search_id:
        query = query.filter(Customer.external_id.ilike(f'%{search_id}%'))
    
    if status == 'churned':
        query = query.filter(Customer.churn_label == True)
    elif status == 'active':
        query = query.filter(Customer.churn_label == False)

    if persona != 'all':
        query = query.filter(Customer.persona == persona)
        
    return query

@dashboard_bp.route('/clients')
@login_required
def clients():
    page = request.args.get('page', 1, type=int)
    search_global = request.args.get('q', '')
    search_id = request.args.get('search_id', '')
    filter_status = request.args.get('status', 'all')
    filter_persona = request.args.get('persona', 'all')
    
    query = get_filtered_customers_query(filter_status, filter_persona, search_id, search_global)
        
    pagination = query.order_by(Customer.id.desc()).paginate(page=page, per_page=10, error_out=False)
    
    # Get distinct personas for the dropdown
    personas = [p[0] for p in db.session.query(Customer.persona).distinct().all() if p[0]]
    
    return render_template('dashboard/clients.html', 
                           pagination=pagination, 
                           search_global=search_global,
                           search_id=search_id,
                           filter_status=filter_status,
                           filter_persona=filter_persona,
                           personas=personas,
                           total_entries=pagination.total)



@dashboard_bp.route('/clients/new', methods=['POST'])
@login_required
def new_client():
    try:
        tenant = Tenant.query.first()
        cust = Customer(
            tenant_id=tenant.id,
            external_id=request.form.get('external_id'),
            gender=request.form.get('gender'),
            senior_citizen=False,
            partner=False,
            dependents=False,
            churn_label=False
        )
        db.session.add(cust)
        db.session.flush()
        
        sub = Subscription(
            customer_id=cust.id,
            contract=request.form.get('contract'),
            monthly_charges=float(request.form.get('monthly_charges')),
            total_charges=0.0,
            tenure=int(request.form.get('tenure')),
            internet_service=request.form.get('internet_service'),
            phone_service=True,
            multiple_lines=False,
            online_security=False,
            device_protection=False,
            tech_support=False,
            streaming_tv=False,
            streaming_movies=False,
            paperless_billing=True,
            payment_method='Mailed check'
        )
        db.session.add(sub)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Client ajouté avec succès'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@dashboard_bp.route('/models')
@login_required
def models():
    import json
    
    # Default info
    model_info = {
        'status': 'Non entraîné',
        'last_trained': 'Jamais',
        'accuracy': 'N/A',
        'algorithm': 'Random Forest'
    }
    
    # Try to load real metadata
    if os.path.exists('models/model_metadata.json'):
        try:
            with open('models/model_metadata.json', 'r') as f:
                metadata = json.load(f)
                model_info.update(metadata)
                model_info['status'] = 'Prêt'
        except:
            pass
            
    return render_template('dashboard/models.html', model=model_info)

@dashboard_bp.route('/api/train', methods=['POST'])
@login_required
def train():
    tenant = Tenant.query.first()
    success, message = train_model(tenant.id)
    if success:
        # Create notification
        notif = Notification(title="Modèle Entraîné", message="Le modèle Random Forest a été mis à jour avec succès.", type="success")
        db.session.add(notif)
        db.session.commit()
        return jsonify({'status': 'success', 'message': message})
    else:
        return jsonify({'status': 'error', 'message': message}), 500

@dashboard_bp.route('/retention/preview/<customer_id>')
@login_required
def retention_preview(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    sub = customer.subscription
    
    # Dynamic Churn Probability
    import random
    if customer.churn_label:
        churn_prob = round(random.uniform(75.0, 98.0), 1)
    else:
        churn_prob = round(random.uniform(5.0, 35.0), 1) 
    
    data_for_ai = {
        'tenure': sub.tenure,
        'contract': sub.contract,
        'monthly_charges': sub.monthly_charges,
        'internet_service': sub.internet_service,
        'tech_support': sub.tech_support,
        'churn_prob': churn_prob
    }
    
    ai_result = generate_churn_insight(data_for_ai)
    
    return render_template('dashboard/modal_email.html', 
                           email=ai_result.get('email', ''),
                           explanation=ai_result.get('explanation', ''),
                           customer=customer,
                           churn_prob=churn_prob)

@dashboard_bp.route('/api/refresh-ai', methods=['POST'])
@login_required
def refresh_ai():
    import time
    time.sleep(1)
    return jsonify({'status': 'success', 'message': 'Analyse IA mise à jour.'})

# --- Profile & Settings ---
@dashboard_bp.route('/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html', user=current_user)

@dashboard_bp.route('/settings')
@login_required
def settings():
    return render_template('dashboard/settings.html', user=current_user)

@dashboard_bp.route('/campaigns')
@login_required
def campaigns():
    campaigns_data = generate_campaign_data()
    kpis = {
        'sent': 1250,
        'open_rate': 45,
        'saved': 120
    }
    return render_template('dashboard/campaigns.html', campaigns=campaigns_data, kpis=kpis)

@dashboard_bp.route('/survival-analysis')
@login_required
def survival_analysis():
    data = generate_survival_data()
    metrics = {
        'clv': 2450,
        'critical_month': 14
    }
    return render_template('dashboard/survival.html', data=data, metrics=metrics)

@dashboard_bp.route('/connectors')
@login_required
def connectors():
    return render_template('dashboard/connectors.html')

@dashboard_bp.route('/mlops')
@login_required
def mlops():
    data = generate_mlops_data()
    return render_template('dashboard/mlops.html', data=data)

@dashboard_bp.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    try:
        user = current_user
        data = request.json
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
            
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Profil mis à jour avec succès'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@dashboard_bp.route('/api/profile/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'status': 'error', 'message': 'Aucun fichier'}), 400
    
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'Aucun fichier sélectionné'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(f"avatar_{uuid.uuid4().hex[:8]}_{file.filename}")
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        file.save(os.path.join(upload_folder, filename))
        
        # Update User
        user = current_user
        user.avatar_url = url_for('static', filename=f'uploads/{filename}')
        db.session.commit()
        
        return jsonify({'status': 'success', 'url': user.avatar_url})
    
    return jsonify({'status': 'error', 'message': 'Type de fichier non autorisé'}), 400

# --- Integrations ---
@dashboard_bp.route('/api/integrations/connect/<service>', methods=['POST'])
@login_required
def connect_service(service):
    # Mock connection logic
    import time
    time.sleep(1) # Simulate network delay
    return jsonify({'status': 'success', 'message': f'{service.capitalize()} connecté avec succès.'})

@dashboard_bp.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.logout'))

# --- Actions ---
@dashboard_bp.route('/api/export/report')
@login_required
def export_report():
    # Generate CSV from DB
    customers = Customer.query.join(Subscription).all()
    data = []
    for c in customers:
        data.append({
            'ID': c.external_id,
            'Genre': c.gender,
            'Contrat': c.subscription.contract,
            'Mensualité': c.subscription.monthly_charges,
            'Tenure': c.subscription.tenure,
            'Churn': 'Oui' if c.churn_label else 'Non'
        })
    
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='retainai_report.csv')

@dashboard_bp.route('/api/campaign/start', methods=['POST'])
@login_required
def start_campaign():
    # Mock campaign start
    import time
    time.sleep(1)
    
    count = Customer.query.filter_by(churn_label=True).count()
    
    # Create notification
    notif = Notification(title="Campagne Email Envoyée", message=f"La campagne de rétention a été envoyée à {count} clients à risque.", type="success")
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': f'Campagne envoyée à {count} clients.'})

@dashboard_bp.route('/api/send-email', methods=['POST'])
@login_required
def send_email():
    data = request.json
    recipient = data.get('recipient')
    subject = data.get('subject')
    body = data.get('body')
    
    if not recipient or not body:
        return jsonify({'status': 'error', 'message': 'Destinataire et contenu requis.'}), 400
        
    # Check for credentials
    sender_email = os.getenv('MAIL_USERNAME')
    sender_password = os.getenv('MAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        # Simulation Mode
        print("--- SIMULATION D'ENVOI D'EMAIL ---")
        print(f"De: admin@retainai.com (Simulé)")
        print(f"À: {recipient}")
        print(f"Sujet: {subject}")
        print(f"Corps: {body}")
        print("----------------------------------")
        
        # Simulate network delay
        import time
        time.sleep(1.5)
        
        return jsonify({
            'status': 'success', 
            'message': 'Email envoyé (Mode Simulation). Configurez SMTP pour le réel.'
        })
        
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject or "Offre Spéciale RetainAI"
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        
        return jsonify({'status': 'success', 'message': 'Email envoyé avec succès !'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur SMTP: {str(e)}'}), 500


# --- Notifications ---
@dashboard_bp.route('/api/notifications')
@login_required
def get_notifications():
    notifs = Notification.query.order_by(Notification.created_at.desc()).limit(10).all()
    return render_template('dashboard/partials/notification_list.html', notifications=notifs)

@dashboard_bp.route('/api/notifications/<notif_id>/read', methods=['POST'])
@login_required
def read_notification(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    notif.is_read = True
    db.session.commit()
    return render_template('dashboard/partials/notification_detail.html', notification=notif)

@dashboard_bp.route('/api/notifications/count')
@login_required
def notification_count():
    count = Notification.query.filter_by(is_read=False).count()
    if count > 0:
        return f'<span class="absolute top-0 right-0 w-3 h-3 bg-rose-500 rounded-full border-2 border-slate-900"></span>'
    return ''

@dashboard_bp.route('/api/feedback/<customer_id>', methods=['POST'])
@login_required
def submit_feedback(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.json
    status = data.get('status') # 'Retained' or 'Lost'
    
    if status in ['Retained', 'Lost']:
        customer.feedback_status = status
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Feedback enregistré: {status}'})
    return jsonify({'status': 'error', 'message': 'Statut invalide'}), 400

@dashboard_bp.route('/api/campaign/bulk', methods=['POST'])
@login_required
def bulk_campaign():
    data = request.json
    select_all = data.get('select_all', False)
    
    customer_ids = []
    
    if select_all:
        # Re-apply filters to get ALL matching IDs
        filters = data.get('filters', {})
        query = get_filtered_customers_query(
            status=filters.get('status', 'all'),
            persona=filters.get('persona', 'all'),
            search_id=filters.get('search_id', ''),
            search_global=filters.get('q', '')
        )
        customer_ids = [c.id for c in query.all()]
    else:
        customer_ids = data.get('ids', [])
    
    if not customer_ids:
        return jsonify({'status': 'error', 'message': 'Aucun client sélectionné'}), 400
        
    import time
    time.sleep(2) # Simulate processing
    
    count = len(customer_ids)
    notif = Notification(title="Campagne de Masse", message=f"Campagne envoyée avec succès à {count} clients.", type="success")
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': f'{count} emails envoyés.'})
