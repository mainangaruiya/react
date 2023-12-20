from flask import render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from website import create_app
from website.models import db, Property, User
import os

app = create_app()
with app.app_context():
    db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def save_and_get_filename(file):
    if file:
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(app.root_path, 'properties')
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))
        return filename
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    user = get_user_somehow()  # Implement this function to get the user
    login_user(user)
    flash('Login successful!', 'success')
    return redirect(url_for('views.buy'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return render_template('logout.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/account')

def account():
    user_email = current_user.email
    user_properties = Property.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', user_email=user_email, user_properties=user_properties)

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        try:
            property_title = request.form['propertyTitle']
            num_bedrooms = request.form['numBedrooms']
            property_location = request.form['propertyLocation']
            price = request.form['price']

            property_video_file = request.files['propertyVideo']

            if property_video_file and allowed_file(property_video_file.filename):
                # Save the file locally
                filename = secure_filename(property_video_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                property_video_file.save(file_path)

                # Add the property to the database with the relative path
                new_property = Property(
                    property_title=property_title,
                    num_bedrooms=num_bedrooms,
                    property_location=property_location,
                    price=price,
                    property_video=f'static/uploads/{filename}',  # Store the relative path
                    user_id=current_user.id
                )

                db.session.add(new_property)
                db.session.commit()

                flash('Property added successfully!', 'success')
                return redirect(url_for('views.sell'))

            else:
                flash('Invalid file format. Allowed formats: mp4, avi, mov, mkv', 'error')

        except Exception as e:
            flash(f'Error adding property: {str(e)}', 'error')

    return render_template('sell.html')

def save_and_get_filename(file):
    if file:
        filename = secure_filename(file.filename)
        file.save(f'properties/{filename}')  # Change 'your_upload_folder' to your desired upload folder
        return filename
    return None


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
