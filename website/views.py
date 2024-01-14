from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
import os
from .models import Property
from . import db



views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        try:
            property_title = request.form['propertyTitle']
            num_bedrooms = request.form['numBedrooms']
            property_location = request.form['propertyLocation']
            price = request.form['price']

            property_video_file = request.files['propertyVideo']
            property_video = save_and_get_filename(property_video_file)

            # Store property information in a text file within the properties folder
            with open(f'{property_video}.txt', 'w') as f:
                f.write(f"Title: {property_title}\n")
                f.write(f"Bedrooms: {num_bedrooms}\n")
                f.write(f"Location: {property_location}\n")
                f.write(f"Price: {price}\n")
                f.write(f"Video: {property_video}\n")
                f.write(f"User ID: {current_user.id}\n")

            flash('Property added successfully!', 'success')
            return redirect(url_for('views.sell'))

        except Exception as e:
            flash(f'Error adding property: {str(e)}', 'error')

    return render_template('sell.html')

@views.route('/buy', methods=['GET'])
def buy():
    all_properties = [p for p in os.listdir(current_app.config['UPLOAD_FOLDER']) if p.endswith('.txt')]
    return render_template('buy.html', all_properties=all_properties)

@views.route('/login', methods=['POST'])
def login():
    user = get_user_somehow()
    login_user(user)
    flash('Login successful!', 'success')
    return redirect(url_for('account.html'))

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return render_template('logout.html')

@views.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@views.route('/account')
@login_required
def account():
    user_email = current_user.email if current_user.is_authenticated else None
    user_properties = Property.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', user_email=user_email, user_properties=user_properties)
