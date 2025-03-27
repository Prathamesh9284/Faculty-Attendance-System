# Faculty Attendance System

The **Faculty Attendance System** is an AI-powered application that automates faculty attendance tracking using face recognition technology. By integrating Mediapipe for facial detection and Firebase for data management, the system offers a seamless and efficient solution for educational institutions.

## Features

- **Face Recognition**: Utilizes Mediapipe to detect and recognize faculty members' faces for accurate attendance marking.
- **Real-time Attendance**: Captures attendance in real-time, reducing manual errors and saving time.
- **Data Management with Firebase**: Stores attendance records securely in Firebase, facilitating easy access and management.
- **Excel Report Generation**: Automatically generates Excel reports of attendance records for administrative use.

## Technologies Used

- **Python**: Serves as the primary programming language for the application.
- **Mediapipe**: Provides efficient face detection and recognition capabilities.
- **Firebase**: Handles backend data storage and management.
- **OpenCV**: Assists in image processing tasks.
- **Pandas**: Used for data manipulation and report generation.

## Installation

Follow these steps to set up the Faculty Attendance System on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Prathamesh9284/Faculty-Attendance-System.git
   cd Faculty-Attendance-System
   ```


2. **Install Dependencies**:
   Ensure you have Python installed on your system. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```


3. **Configure Firebase**:
   - Set up a Firebase project and obtain the Firebase configuration file (`serviceAccountKey.json`).
   - Place the `serviceAccountKey.json` file in the project directory.

4. **Prepare Face Encodings**:
   - Collect images of faculty members and store them in the `static` directory.
   - Run the `encoder.py` script to generate face encodings and create the `encoding.pkl` file.

5. **Run the Application**:
   Start the application using the following command:
   ```bash
   python app.py
   ```


## Usage

- **Marking Attendance**:
  - The application captures real-time video input and recognizes faculty members' faces to mark attendance.
  - Attendance records are stored in Firebase and can be accessed for verification.

- **Generating Reports**:
  - Attendance data can be exported as Excel files, which are saved in the `generated_excels` directory.

## Configuration

- **Firebase Setup**: Ensure that the Firebase project is correctly configured and the `serviceAccountKey.json` file is placed in the project directory.
- **Directory Structure**:
  - `static`: Contains images of faculty members used for face recognition.
  - `templates`: Holds HTML templates for the application's user interface.
  - `generated_excels`: Stores generated Excel reports of attendance records.
