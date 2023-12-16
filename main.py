from flask import render_template, request
from website import create_app
from website.models import db, Property, User  # Import db from models.py
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from website.views import views

app = create_app()
app.register_blueprint(views, name='views_blueprint')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Your existing routes and configurations...

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/account')
@login_required
def account():
    # Retrieve user information
    user_email = current_user.email

    # Retrieve properties posted by the current user
    user_properties = Property.query.filter_by(user_id=current_user.id).all()

    return render_template('account.html', user=user)

@app.route('/buy')
def buy():
    # Retrieve properties from the database
    properties = Property.query.all()

    # Render the buy.html template and pass the properties to it
    return render_template('buy.html', properties=properties)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
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
        new_property = Property(kitchen_image=kitchen_image,
            sitting_room_image=sitting_room_image,
            master_bedroom_image=master_bedroom_image,
            additional_images=','.join(additional_images),
            property_title=property_title,
            num_bedrooms=num_bedrooms,
            property_location=property_location,
            price=price)

        # Add the new property to the database
        db.session.add(new_property)
        db.session.commit()

        # Render the sell.html template
        return render_template('sell.html',
            kitchen_image=kitchen_image,
            sitting_room_image=sitting_room_image,
            master_bedroom_image=master_bedroom_image,
            additional_images=additional_images,
            property_title=property_title,
            num_bedrooms=num_bedrooms,
            property_location=property_location,
            price=price)

    # If the request method is GET, simply render the sell.html template
    return render_template('sell.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables only if they don't exist
    app.run(debug=True)
