from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Property
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        try:
            # Retrieve form data
            kitchen_image = request.form['kitchenImage']
            sitting_room_image = request.form['sittingRoomImage']
            master_bedroom_image = request.form['masterBedroomImage']
            
            # Retrieve additional images dynamically
            additional_images = []
            for i in range(1, 4):
                image_key = f'additionalImage{i}'
                if image_key in request.form:
                    additional_images.append(request.form[image_key])

            # Retrieve other form data
            property_title = request.form['propertyTitle']
            num_bedrooms = request.form['numBedrooms']
            property_location = request.form['propertyLocation']
            price = request.form['price']  # Add this line to retrieve the price

            # Perform any additional logic or validation here

            # Create a new Property instance
            new_property = Property(
                kitchen_image=kitchen_image,
                sitting_room_image=sitting_room_image,
                master_bedroom_image=master_bedroom_image,
                additional_images=','.join(additional_images),
                property_title=property_title,
                num_bedrooms=num_bedrooms,
                property_location=property_location,
                price=price,
                user_id=current_user.id
            )

            # Add the new property to the database
            db.session.add(new_property)
            db.session.commit()

            # Flash success message
            flash('Property added successfully!', 'success')

            # Redirect to another page or render template
            return redirect(url_for('views.sell'))

        except Exception as e:
            # Flash error message
            flash(f'Error adding property: {str(e)}', 'error')

    # If the request method is GET, simply render the sell.html template
    return render_template('sell.html')

@views.route('/buy', methods=['GET'])
@login_required
def buy():
    all_properties = Property.query.all()

    # Render the buy.html template and pass the properties to it
    return render_template('buy.html', all_properties=all_properties)

@views.route('/login', methods=['POST'])
def login():
    login_user(user)
    return redirect(url_for('views.buy'))


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@views.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')


@views.route('/account')
@login_required
def account():
    # Use the `current_user` provided by Flask-Login
    user_email = current_user.email if current_user.is_authenticated else None
    # Retrieve properties posted by the current user
    user_properties = Property.query.filter_by(user_id=current_user.id).all()

    return render_template('account.html', user_email=user_email, user_properties=user_properties)