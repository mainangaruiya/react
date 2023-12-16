from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Property
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

@views.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        # Retrieve form data
        kitchen_image = request.files['kitchenImage']
        sitting_room_image = request.files['sittingRoomImage']
        dinning_room_image = request.files['dinningRoomImage']
        master_bedroom_image = request.files['masterBedroomImage']

        # Process the file uploads as needed
        # For example, you can save the files to a folder on your server

        # Rest of your existing code for handling other form data...

        # Create a new Property instance
        new_property = Property(
            kitchen_image=kitchen_image.filename,
            sitting_room_image=sitting_room_image.filename,
            dinning_room_image=dinning_room_image.filename,
            master_bedroom_image=master_bedroom_image.filename,
            # ... (other property fields)
        )

        # Save the files to a folder on your server
        # You may want to check for allowed file types, handle file names, etc.
        kitchen_image.save('path/to/your/folder/' + kitchen_image.filename)
        sitting_room_image.save('path/to/your/folder/' + sitting_room_image.filename)
        dinning_room_image.save('path/to/your/folder/' + dinning_room_image.filename)
        master_bedroom_image.save('path/to/your/folder/' + master_bedroom_image.filename)

        # ... (rest of your existing code)

    # Render the sell.html template for both GET and POST requests
    return render_template('sell.html')

# Add any other routes if needed
@views.route('/buy')
def buy():
    # Retrieve properties from the database
    properties = Property.query.all()
    return render_template('buy.html', properties=properties)

@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@views.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

