from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    bookings = db.relationship('Booking', backref='user', lazy=True)

# New UNESCO-related models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    sites = db.relationship('Site', backref='category')

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    sites = db.relationship('Site', backref='region')

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    sites = db.relationship('Site', secondary='site_state')

class IsoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alpha_2_code = db.Column(db.String(2))
    sites = db.relationship('Site', secondary='site_iso_code')

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

class SiteState(db.Model):
    __tablename__ = 'site_state'
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), primary_key=True)

class SiteIsoCode(db.Model):
    __tablename__ = 'site_iso_code'
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), primary_key=True)
    iso_code_id = db.Column(db.Integer, db.ForeignKey('iso_code.id'), primary_key=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monument_name = db.Column(db.String(200), nullable=False)
    booking_date = db.Column(db.DateTime(timezone=True), default=func.now())
    visit_date = db.Column(db.Date, nullable=False)
    visitors = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    special_requests = db.Column(db.Text)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            'monument_name': self.monument_name,
            'booking_date': self.booking_date.strftime('%Y-%m-%d'),
            'visit_date': self.visit_date.strftime('%Y-%m-%d'),
            'visitors': self.visitors,
            'total_amount': self.total_amount,
            'status': self.status,
            'special_requests': self.special_requests,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }