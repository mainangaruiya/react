from flask import render_template, request
from website import create_app
from flask_sqlalchemy import SQLAlchemy
from website.models import Property

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database
db = SQLAlchemy(app)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kitchen_image = db.Column(db.String(100))
    sitting_room_image = db.Column(db.String(100))
    living_room_image = db.Column(db.String(100))
    master_bedroom_image = db.Column(db.String(100))
    additional_images = db.Column(db.String(255))
    property_title = db.Column(db.String(100))
    num_bedrooms = db.Column(db.Integer)
    property_location = db.Column(db.String(100))
    price = db.Column(db.Float)  # Add the price field to your model

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buy')
def buy():
    # Retrieve search parameters from the query string
    num_bedrooms = request.args.get('numBedrooms', type=int)
    property_location = request.args.get('propertyLocation', type=str)
    property_title = request.args.get('propertyTitle', type=str)
    price = request.args.get('price', type=float)

    # Query properties based on search parameters
    query = Property.query
    if num_bedrooms is not None:
        query = query.filter_by(num_bedrooms=num_bedrooms)
    if property_location:
        query = query.filter(Property.property_location.ilike(f'%{property_location}%'))
    if property_title:
        query = query.filter(Property.property_title.ilike(f'%{property_title}%'))
    if price is not None:
        query = query.filter(Property.price == price)

    # Retrieve filtered properties from the database
    properties = query.all()

    # Render the buy.html template and pass the filtered properties to it
    return render_template('buy.html', properties=properties)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
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
        price = request.form['price']  # Add this line to retrieve the price

        # Perform any additional logic or validation here

        # Create a new Property instance
        new_property = Property(kitchen_image=kitchen_image,
                               sitting_room_image=sitting_room_image,
                               living_room_image=living_room_image,
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
                               living_room_image=living_room_image,
                               master_bedroom_image=master_bedroom_image,
                               additional_images=additional_images,
                               property_title=property_title,
                               num_bedrooms=num_bedrooms,
                               property_location=property_location,
                               price=price)

    # If the request method is GET, simply render the sell.html template
    return render_template('sell.html')

if __name__ == '__main__':
    db.create_all()  # Create the database tables before running the app
    app.run(debug=True)
