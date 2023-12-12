from flask import render_template, request
from website import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buy')
def buy():
    return render_template('buy.html')

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

        # Perform any additional logic or validation here

        # Render the base.html template and pass the data to it
        return render_template('base.html', kitchen_image=kitchen_image, sitting_room_image=sitting_room_image)

    # If the request method is GET, simply render the base.html template
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
