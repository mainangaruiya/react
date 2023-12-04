from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/loggin')
def login():
    return render_template('login.html')

@app.route('/listing', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        # Process the form data here
        property_type = request.form['propertyType']
        property_images = request.files.getlist('propertyImages')[:8]  # Get up to 8 images
        property_description = request.form['propertyDescription']
       
    return render_template('sell.html')

if __name__ == '__main__':
    app.run(debug=True)
