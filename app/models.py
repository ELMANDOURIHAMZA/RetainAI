from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    users = db.relationship('User', backref='tenant', lazy=True)
    customers = db.relationship('Customer', backref='tenant', lazy=True)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='analyst')
    name = db.Column(db.String(100), default='Admin User')
    avatar_url = db.Column(db.String(255), default='https://ui-avatars.com/api/?name=Admin+User&background=random')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    type = db.Column(db.String(50), default='info') # info, warning, success, error

class RiskHistory(db.Model):
    __tablename__ = 'risk_history'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    risk_score = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipients_count = db.Column(db.Integer)
    conversion_rate = db.Column(db.Float, default=0.0)

# Update Customer Model with new fields (Simulated by adding them here, requires DB recreation)
# We are redefining the class to include new columns. 
# In a real migration we would use Alembic, here we will rely on seed_data.py to recreate DB.
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    external_id = db.Column(db.String(50), nullable=False)
    
    # Demographics
    gender = db.Column(db.String(20))
    senior_citizen = db.Column(db.Boolean)
    partner = db.Column(db.Boolean)
    dependents = db.Column(db.Boolean)
    
    # Status & Advanced Analytics
    churn_label = db.Column(db.Boolean, default=False)
    persona = db.Column(db.String(50), default='Standard') # Price Sensitive, Tech Reliant, etc.
    feedback_status = db.Column(db.String(20), default='Pending') # Pending, Retained, Lost
    ab_test_group = db.Column(db.String(10), default='A') # A or B
    
    subscription = db.relationship('Subscription', backref='customer', uselist=False, lazy=True)
    predictions = db.relationship('Prediction', backref='customer', lazy=True)
    insights = db.relationship('AIInsight', backref='customer', lazy=True)
    risk_history = db.relationship('RiskHistory', backref='customer', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    
    # Services
    phone_service = db.Column(db.Boolean)
    multiple_lines = db.Column(db.Boolean)
    internet_service = db.Column(db.String(50)) # DSL, Fiber optic, No
    online_security = db.Column(db.Boolean)
    device_protection = db.Column(db.Boolean)
    tech_support = db.Column(db.Boolean)
    streaming_tv = db.Column(db.Boolean)
    streaming_movies = db.Column(db.Boolean)
    
    # Contract & Billing
    contract = db.Column(db.String(50)) # Month-to-month, One year, Two year
    paperless_billing = db.Column(db.Boolean)
    payment_method = db.Column(db.String(50))
    monthly_charges = db.Column(db.Float)
    total_charges = db.Column(db.Float)
    tenure = db.Column(db.Integer)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    score = db.Column(db.Float) # 0.0 to 1.0
    risk_level = db.Column(db.String(20)) # Low, Medium, High
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)

class AIInsight(db.Model):
    __tablename__ = 'ai_insights'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    insight_text = db.Column(db.Text)
    retention_email_draft = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True) # Nullable for system-wide
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50), default='info') # info, warning, success, error
