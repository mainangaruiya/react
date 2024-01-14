from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from website import create_app, db
from website.models import User, Property
from website.views import views
import os


app.register_blueprint(views)

app = create_app()
UPLOAD_FOLDER = os.path.join(app.root_path, 'properties')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_and_get_filename(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename, file_path
    return None, None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    user = get_user_somehow()  # Implement this function to get the user
    login_user(user)
    flash('Login successful!', 'success')
    return redirect(url_for('sell'))

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
@login_required
def account():
    user_email = current_user.email
    user_properties = Property.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', user_email=user_email, user_properties=user_properties)

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        try:
            property_title = request.form['propertyTitle']
            num_bedrooms = request.form['numBedrooms']
            property_location = request.form['propertyLocation']
            price = request.form['price']

            property_video_file = request.files['propertyVideo']

            filename, file_path = save_and_get_filename(property_video_file)

            if filename:
                # Store property information in the database
                new_property = Property(
                    property_title=property_title,
                    num_bedrooms=num_bedrooms,
                    property_location=property_location,
                    price=price,
                    property_video=file_path,
                    user_id=current_user.id
                )

                db.session.add(new_property)
                db.session.commit()

                flash('Property added successfully!', 'success')
                return redirect(url_for('sell'))

            else:
                flash('Invalid file format. Allowed formats: mp4, avi, mov, mkv', 'error')

        except Exception as e:
            flash(f'Error adding property: {str(e)}', 'error')

    return render_template('sell.html')

if __name__ == '__main__':
    with app.app_context():
         from website.models import db
        db.create_all()
    app.run(debug=True)
