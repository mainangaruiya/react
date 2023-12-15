from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

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

# Add the following route for selling
@views.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    # Retrieve form data
    kitchen_image = request.form['kitchenImage']
    sitting_room_image = request.form['sittingRoomImage']
    living_room_image = request.form['livingRoomImage']
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
    price = request.form['price']

    # Perform any additional logic or validation here

    # Create a new Property instance
    new_property = Property(
        kitchen_image=kitchen_image,
        sitting_room_image=sitting_room_image,
        living_room_image=living_room_image,
        master_bedroom_image=master_bedroom_image,
        additional_images=','.join(additional_images),
        property_title=property_title,
        num_bedrooms=num_bedrooms,
        property_location=property_location,
        price=price
    )

    # Add the new property to the database
    db.session.add(new_property)
    db.session.commit()

    # Render the sell.html template
    return render_template('sell.html',
                           kitchen_image=kitchen_image,
                           sitting_room_image=sitting_room_image,
                           living_room_image=living_room_image,
                           master_bedroom_image=master_bedroom_image,
                           additional_images=additional_images,
                           property_title=property_title,
                           num_bedrooms=num_bedrooms,
                           property_location=property_location,
                           price=price)

# Add any other routes if needed
