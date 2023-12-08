# main.py

from flask import render_template, request
from website import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('property_upload.html')

@app.route('/sell', methods=['POST'])
def sell():
    if request.method == 'POST':
        # Retrieve form data
        kitchen_image = request.form['kitchenImage']
        sitting_room_image = request.form['sittingRoomImage']
        # Add more fields as needed

        # Perform any additional logic or validation here

        # Render the sell.html template and pass the data to it
        return render_template('sell.html', kitchen_image=kitchen_image, sitting_room_image=sitting_room_image)

if __name__ == '__main__':
    app.run(debug=True)
