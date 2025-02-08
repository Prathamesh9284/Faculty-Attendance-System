import os
import firebase_admin
import pandas as pd
from firebase_admin import credentials, db
from flask import Flask, render_template, request, send_file

# Initialize Flask app
app = Flask(__name__)

# Firebase Admin SDK setup
cred = credentials.Certificate("sihp-2135d-firebase-adminsdk-p2uhe-2490ca71b7.json")  # Path to your Firebase service account JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sihp-2135d-default-rtdb.firebaseio.com/'
})

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to download the data in Excel format
@app.route('/download', methods=['POST'])
def download_data():
    date = request.form.get('date')
    if not date:
        return "Please select a date", 400

    # Firebase reference to fetch data
    ref = db.reference(f'face_predictions/{date}')
    snapshot = ref.get()

    if snapshot is None:
        return "No data found for this date", 404

    # Convert the data to a Pandas DataFrame
    records = []
    for record in snapshot.values():
        records.append(record)

    df = pd.DataFrame(records)

    # Save the DataFrame to an Excel file
    file_path = f"E:\DLIB\generated_excelsdata_{date}.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')

    # Send the Excel file to the user
    return send_file(file_path, as_attachment=True, download_name=f"face_predictions_{date}.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
