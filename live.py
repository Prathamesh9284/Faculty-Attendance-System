import face_recognition
import cv2
import pickle
import os
import time
from collections import Counter
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

# Firebase Admin SDK setup
cred = credentials.Certificate("sihp-2135d-firebase-adminsdk-p2uhe-2490ca71b7.json")  # Path to your Firebase service account JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sihp-2135d-default-rtdb.firebaseio.com/'
})

# Load encodings from the pickle file
def load_encodings_from_file(filename):
    """Load encodings from a pickle file."""
    if not os.path.exists(filename):
        print(f"Error: Encoding file not found - {filename}")
        return None

    with open(filename, 'rb') as f:
        return pickle.load(f)

# Draw a label above the detected face
def draw_label(frame, name, top, right, bottom, left):
    """Draw a label with a name above the face rectangle."""
    # Draw a rectangle around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    # Draw the label with the name
    cv2.rectangle(frame, (left, top - 20), (right, top), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, name, (left + 5, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Constants
ENCODING_FILE = 'encoding.pkl'
THRESHOLD = 0.45  # Adjust as needed; lower values are stricter
UPDATE_INTERVAL = 30  # Time interval in seconds to update the database
MAJORITY_WINDOW = 5  # Number of frames to accumulate predictions for majority voting
DATE_FORMAT = "%Y-%m-%d"  # To store records by day

# Load the saved encodings
encodings_data = load_encodings_from_file(ENCODING_FILE)
if encodings_data is None:
    print("Failed to load encodings. Exiting.")
    exit()

# Initialize variables for majority voting and tracking last update time
face_predictions = {}  # Store predictions for faces
last_update_time = {}  # Store the last time a person was updated in the database

# Start video capture
video_capture = cv2.VideoCapture(0)  # 0 for the default camera

print("Starting camera. Press 'q' to quit.")

def get_today_date():
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime(DATE_FORMAT)

def store_prediction_in_db(name, timestamp):
    """Store the prediction in Firebase only once per day for each person."""
    today_date = get_today_date()

    # Check if record already exists for the current date
    ref = db.reference(f'face_predictions/{today_date}')
    snapshot = ref.get()

    if snapshot is None:
        # No record for today, create new
        ref.push({
            'name': name,
            'timestamp': timestamp
        })
    else:
        # Check if the person already has a record for today
        for record in snapshot.values():
            if record['name'] == name:
                return  # Record already exists for today

        # If not, create new record
        ref.push({
            'name': name,
            'timestamp': timestamp
        })

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Resize frame dynamically
    resize_factor = 1.0  # Adjust factor based on testing (e.g., 0.5 or 1.0)
    small_frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Initialize a list to store the names
    predicted_names = []

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Scale back up face locations since the frame was resized
        top = int(top / resize_factor)
        right = int(right / resize_factor)
        bottom = int(bottom / resize_factor)
        left = int(left / resize_factor)

        # Compare face encoding with saved encodings
        matches = face_recognition.compare_faces(list(encodings_data.values()), face_encoding, tolerance=THRESHOLD)
        name = "Unknown"

        # Use the shortest distance to decide the best match
        face_distances = face_recognition.face_distance(list(encodings_data.values()), face_encoding)
        best_match_index = face_distances.argmin() if len(face_distances) > 0 else None

        if best_match_index is not None and matches[best_match_index]:
            name = list(encodings_data.keys())[best_match_index].split('.')[0]  # Use filename without extension

        # Append the name to the predicted names list
        predicted_names.append(name)

        # Draw the name above the face
        draw_label(frame, name, top, right, bottom, left)

    if predicted_names:
        # Get the most common name excluding "Unknown"
        name_counts = Counter(predicted_names)
        most_common_name, most_common_count = name_counts.most_common(1)[0]

        if most_common_name == "Unknown" and len(name_counts) > 1:
            # If "Unknown" is the most common, get the second most frequent prediction
            name_counts.pop("Unknown")
            second_most_common_name = name_counts.most_common(1)[0][0]
            name = second_most_common_name
        else:
            name = most_common_name
    else:
        # If no names are predicted, set a default name or skip
        name = "No Face Detected"

    # Track face appearances and update database after 30 seconds
    if name != "No Face Detected" and name != "Unknown":
        current_time = time.time()
        if name not in last_update_time or current_time - last_update_time[name] >= UPDATE_INTERVAL:
            store_prediction_in_db(name, current_time)
            last_update_time[name] = current_time

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
video_capture.release()
cv2.destroyAllWindows()
