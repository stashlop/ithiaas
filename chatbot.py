from flask import Blueprint, request, jsonify, session
import re
from . import nlp

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    response_text = get_extended_response(user_message)
    return jsonify({"response": response_text})

def extract_booking_details(text):
    doc = nlp(text)
    date = None
    tickets = None
    for ent in doc.ents:
        if ent.label_ == "DATE" and not date:
            date = ent.text
        elif ent.label_ == "CARDINAL" and not tickets:
            tickets = ent.text
    return date, tickets

def get_extended_response(user_message):
    # Check if we are already in a booking flow
    booking_state = session.get('booking_state', None)
    
    if booking_state == "awaiting_details":
        date, tickets = extract_booking_details(user_message)
        partial_date = session.get('partial_date')
        partial_tickets = session.get('partial_tickets')
        if date:
            partial_date = date
            session['partial_date'] = partial_date
        if tickets:
            partial_tickets = tickets
            session['partial_tickets'] = partial_tickets
        if partial_date and partial_tickets:
            session.pop('booking_state', None)
            session.pop('partial_date', None)
            session.pop('partial_tickets', None)
            return f"Booking confirmed for {partial_date} with {partial_tickets} ticket(s)."
        else:
            missing = []
            if not partial_date:
                missing.append("booking date")
            if not partial_tickets:
                missing.append("number of tickets")
            missing_info = " and ".join(missing)
            return f"Please provide the {missing_info} to complete your booking."
    
    if re.search(r'\b(book|reserve|booking|ticket)\b', user_message, re.IGNORECASE):
        date, tickets = extract_booking_details(user_message)
        if date and tickets:
            return f"Booking confirmed for {date} with {tickets} ticket(s)."
        else:
            session['booking_state'] = "awaiting_details"
            if date:
                session['partial_date'] = date
            if tickets:
                session['partial_tickets'] = tickets
            missing = []
            if not date:
                missing.append("booking date")
            if not tickets:
                missing.append("number of tickets")
            missing_info = " and ".join(missing)
            return f"To complete your booking, please provide the {missing_info}."
    
    if re.search(r'\b(hello|hi|hey)\b', user_message, re.IGNORECASE):
        return "Hello! How can I assist you with your monument booking today?"
    
    return "I'm sorry, I didn't understand that. Could you please rephrase?"
