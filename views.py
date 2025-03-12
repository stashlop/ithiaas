from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Booking
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/index')
@login_required
def place():
    festival_sites = {
        'january': {
            'festivals': ['Makar Sankranti', 'Pongal', 'Lohri', 'Bihu'],
            'sites': ['Great Living Chola Temples', 'Rani-ki-Vav']
        },
        'march': {
            'festivals': ['Holi', 'Maha Shivratri'],
            'sites': ['Khajuraho Group of Monuments', 'Ellora Caves', 'Mahabodhi Temple']
        },
        'august': {
            'festivals': ['Raksha Bandhan', 'Janmashtami', 'Ganesh Chaturthi'],
            'sites': ['Sun Temple Konark', 'Elephanta Caves', 'Jaipur City']
        },
        'october': {
            'festivals': ['Diwali', 'Chhath Puja'],
            'sites': ['Taj Mahal', 'Agra Fort', 'Fatehpur Sikri']
        },
        'december': {
            'festivals': ['Christmas', 'New Year'],
            'sites': ['Churches of Goa', 'Victorian Gothic Mumbai']
        }
    }
    return render_template("index.html", user=current_user, festival_sites=festival_sites)

@views.route('/map')
@login_required
def map_view():
    heritage_sites = [
        {
            "name": "Taj Mahal",
            "description": "An ivory-white marble mausoleum on the right bank of the river Yamuna, commissioned in 1632 by Mughal emperor Shah Jahan.",
            "lat": 27.1751,
            "lng": 78.0421
        },
        {
            "name": "Qutub Minar",
            "description": "A 73-meter tall minaret built in the early 13th century, UNESCO World Heritage site.",
            "lat": 28.5244,
            "lng": 77.1855
        },
        {
            "name": "Ajanta Caves",
            "description": "Ancient Buddhist cave monuments dating from the 2nd century BCE to about 480 CE.",
            "lat": 20.5519,
            "lng": 75.7033
        },
        {
            "name": "Ellora Caves",
            "description": "Archaeological site with Hindu, Buddhist and Jain cave temples built between the 6th and 10th centuries.",
            "lat": 20.0258,
            "lng": 75.1780
        },
        {
            "name": "Khajuraho Group of Monuments",
            "description": "Famous for their nagara-style architectural symbolism and erotic sculptures.",
            "lat": 24.8318,
            "lng": 79.9199
        },
        {
            "name": "Sun Temple Konark",
            "description": "13th-century Sun Temple known for its architectural grandeur and intricate artwork.",
            "lat": 19.8876,
            "lng": 86.0945
        },
        {
            "name": "Hampi",
            "description": "Ancient ruins of Vijayanagara Empire's capital, featuring stunning temple architecture.",
            "lat": 15.3350,
            "lng": 76.4600
        },
        {
            "name": "Fatehpur Sikri",
            "description": "16th-century city served as the capital of the Mughal Empire for a brief period.",
            "lat": 27.0940,
            "lng": 77.6711
        },
        {
            "name": "Sanchi Stupa",
            "description": "Ancient Buddhist monuments dating from the 3rd century BCE to the 12th century CE.",
            "lat": 23.4817,
            "lng": 77.7397
        },
        {
            "name": "Mahabodhi Temple",
            "description": "Ancient temple marking the location where Buddha attained enlightenment.",
            "lat": 24.6959,
            "lng": 84.9914
        },
        {
            "name": "Elephanta Caves",
            "description": "Network of sculpted caves dedicated to Lord Shiva on Elephanta Island.",
            "lat": 18.9633,
            "lng": 72.9315
        },
        {
            "name": "Great Living Chola Temples",
            "description": "11th-12th century temples built during the Chola dynasty.",
            "lat": 10.7870,
            "lng": 79.1320
        },
        {
            "name": "Humayun's Tomb",
            "description": "1570 Mughal architecture that inspired the Taj Mahal.",
            "lat": 28.5933,
            "lng": 77.2507
        },
        {
            "name": "Amber Fort",
            "description": "Majestic fort combining Rajput and Mughal architecture.",
            "lat": 26.9855,
            "lng": 75.8513
        },
        {
            "name": "Mysore Palace",
            "description": "Historical palace and residence of the Wadiyar dynasty.",
            "lat": 12.3052,
            "lng": 76.6552
        }
    ]
    return render_template("map.html", user=current_user, sites=heritage_sites)

@views.route('/booking')
@login_required
def booking():
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("booking.html", user=current_user, today_date=today_date)

@views.route('/book_visit', methods=['POST'])
@login_required
def book_visit():
    if request.method == 'POST':
        monument = request.form.get('monument')
        visit_date = request.form.get('visit_date')
        visitors = request.form.get('visitors')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        special_requests = request.form.get('special_requests')

        # Calculate total amount (base price * number of visitors)
        base_price = 1500
        total_amount = base_price * int(visitors)

        # Create new booking
        new_booking = Booking(
            monument_name=monument,
            visit_date=datetime.strptime(visit_date, '%Y-%m-%d').date(),
            visitors=visitors,
            total_amount=total_amount,
            name=name,
            email=email,
            phone=phone,
            special_requests=special_requests,
            user_id=current_user.id
        )

        try:
            db.session.add(new_booking)
            db.session.commit()
            flash('Booking request received successfully! We will contact you shortly.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while processing your booking. Please try again.', 'error')

        return redirect(url_for('views.booking'))

    return redirect(url_for('views.booking'))

@views.route('/booking-history')
@login_required
def booking_history():
    # Fetch bookings for the current user, ordered by booking date (newest first)
    bookings = Booking.query.filter_by(user_id=current_user.id)\
        .order_by(Booking.booking_date.desc())\
        .all()
    
    # Convert bookings to dictionary format for the template
    bookings_list = [booking.to_dict() for booking in bookings]
    
    return render_template('booking_history.html', user=current_user, bookings=bookings_list)

