# Intrusion Detection System

A Flask-based web application designed to detect network intrusions using a pre-trained SVM model trained on the NSL-KDD dataset. This project provides a user-friendly interface for uploading network logs, viewing prediction history, and visualizing attack distributions, along with a REST API for programmatic access.

## Overview

The Intrusion Detection System (IDS) leverages machine learning to classify network traffic as `Normal` or `Malicious`. Built with Flask, it includes user authentication, a frontend interface for file uploads and visualization, and a backend API for predictions. The system is trained on the NSL-KDD dataset, a widely used benchmark for intrusion detection research, making it a practical tool for learning about network security and machine learning.

## Features
- **User Authentication**: Secure signup, login, and logout functionality using Flask-Login.
- **Intrusion Detection**: Upload `.txt` files in NSL-KDD format to classify network traffic as `Normal` or `Malicious`.
- **Dashboard Visualization**: View prediction history in a table and attack distribution in a bar chart (powered by Chart.js).
- **REST API**: Access predictions programmatically via the `/predict` endpoint.
- **Error Handling**: Gracefully handles invalid file uploads and malformed data with user feedback.

## Technologies Used
- **Backend**:
  - Flask: Web framework for building the application.
  - Flask-SQLAlchemy: ORM for database management.
  - Flask-Login: User authentication and session management.
  - Flask-RESTful: API development for the `/predict` endpoint.
- **Machine Learning**:
  - Scikit-learn: SVM model, PCA for dimensionality reduction, StandardScaler for feature scaling.
  - Pandas: Data manipulation and preprocessing.
  - Imbalanced-learn (SMOTE): Handling imbalanced dataset during training.
- **Frontend**:
  - HTML, CSS, JavaScript: Core web technologies for the user interface.
  - Chart.js: Visualization of attack distribution in the dashboard.
  - Bootstrap 5.3: Styling and responsive design.
- **Database**: SQLite (`site.db`) for storing user data and predictions.
- **Dataset**: NSL-KDD (`KDDTrain+.txt`, `KDDTest+.txt`) for training and testing.

## Project Structure
```
Intrusion-Detection-System/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── chart.js
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── upload.html
│   │   ├── dashboard.html
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
├── data/
│   ├── KDDTrain+.txt
│   ├── KDDTest+.txt
├── model/
│   ├── train_model.py
│   ├── svm_model.pkl
│   ├── scaler.pkl
│   ├── protocol_type_encoder.pkl
│   ├── service_encoder.pkl
│   ├── flag_encoder.pkl
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
```

- `app/`: Contains the Flask application, including templates for the frontend, static files (CSS, JS), and backend logic.
- `data/`: Stores the NSL-KDD dataset files (not tracked in Git due to size limits).
- `model/`: Includes the training script (`train_model.py`) and pre-trained model files (`.pkl`).
- `app.py`: Entry point to run the Flask app.
- `requirements.txt`: Lists Python dependencies.
- `.gitignore`: Excludes `venv/`, `data/`, `.env`, and `site.db` from version control.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **Git**: For cloning the repository.
- **NSL-KDD Dataset**: `KDDTrain+.txt` and `KDDTest+.txt` files, available from the [NSL-KDD website](https://www.unb.ca/cic/datasets/nsl.html).

## Setup Instructions

Follow these steps to set up the project locally and run the application.

### 1. Clone the Repository
Clone the project to your local machine:
```bash
git clone https://github.com/harshues04/Intrusion-Detection-System.git
cd Intrusion-Detection-System
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies
Install the required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Download the NSL-KDD Dataset
- Download `KDDTrain+.txt` and `KDDTest+.txt` from the [NSL-KDD website](https://www.unb.ca/cic/datasets/nsl.html).
- Place them in the `data/` directory:
  ```
  Intrusion-Detection-System/data/
  ├── KDDTrain+.txt
  ├── KDDTest+.txt
  ```
- **Note**: These files are not included in the repository due to GitHub’s file size limit of 100 MB.

### 5. Train the Model
Train the SVM model to generate the necessary `.pkl` files for prediction:
```bash
python model/train_model.py
```
- This script generates the following files in the `model/` directory:
  - `svm_model.pkl`: Pre-trained SVM model.
  - `scaler.pkl`: StandardScaler for feature scaling.
  - `protocol_type_encoder.pkl`, `service_encoder.pkl`, `flag_encoder.pkl`: Label encoders for categorical features.
- **Training Time**: Approximately 10-35 minutes, depending on your hardware (e.g., 4-core CPU, 8-16 GB RAM).

### 6. Initialize the Database
Create the SQLite database (`site.db`) to store user data and prediction history:
```bash
python -c "from app import create_app, db; app = create_app(); with app.app_context(): db.create_all()"
```

### 7. Run the Application
Start the Flask development server:
```bash
python app.py
```
- The app will be accessible at `http://localhost:5000`.

## Testing the Application

This section provides detailed steps to test the application’s core functionalities: user authentication, file upload and prediction, dashboard visualization, API access, and edge cases.

### Prepare Test Files
1. **Create `test.txt`**:
   - Create a file named `test.txt` in the project root with a single NSL-KDD row (42 columns, comma-separated):
     ```
     0,tcp,http,SF,181,5450,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.00,0.00,0.00,0.00,1.00,0.00,0.00,9,9,1.00,0.00,0.11,0.00,0.00,0.00,0.00,0.00,normal,20
     ```
   - This row represents a "normal" network event, expected to be classified as `Normal`.

2. **Create `test_malicious.txt`**:
   - Create a file named `test_malicious.txt` with a known attack row:
     ```
     0,tcp,http,REJ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,123,1,1.00,1.00,0.00,0.00,0.01,0.99,0.00,255,1,0.00,0.60,0.00,0.00,1.00,1.00,0.00,0.00,neptune,21
     ```
   - This row represents a "neptune" attack, expected to be classified as `Malicious`.

### Test User Authentication
1. **Signup**:
   - Navigate to `http://localhost:5000` (redirects to `/login`).
   - Click the "Signup" link to go to `/signup`.
   - Enter username: `testuser`, password: `testpass`, and submit.
   - **Expected**: Redirect to `/login` with a flash message: "Signup successful".

2. **Login**:
   - At `/login`, enter `testuser` and `testpass`, then submit.
   - **Expected**: Redirect to `/upload`.

3. **Logout**:
   - From `/upload`, click "Logout" in the navigation bar.
   - **Expected**: Redirect to `/login`.

### Test File Upload and Prediction
1. **Upload `test.txt`**:
   - Log in as `testuser`.
   - At `/upload`, click "Choose File", select `test.txt`, and click "Analyze".
   - **Expected**: Redirect to `/dashboard`. The prediction history table shows:
     - Filename: `test.txt`
     - Result: `Normal`
     - Timestamp: Current date/time (e.g., `2025-05-16 23:50:xx`)

2. **Upload `test_malicious.txt`**:
   - Repeat the upload process with `test_malicious.txt`.
   - **Expected**: On `/dashboard`, a new row shows:
     - Filename: `test_malicious.txt`
     - Result: `Malicious`
     - Timestamp: Current date/time

### Test Dashboard Visualization
- Navigate to `/dashboard` and verify:
  - **Prediction History Table**: Lists entries for `test.txt` (`Normal`) and `test_malicious.txt` (`Malicious`).
  - **Attack Distribution Chart**: Displays a bar chart with `Normal` (count: 1) and `Malicious` (count: 1).
- **Troubleshooting**: If the chart doesn’t render, check the browser console (F12 → Console) for errors. Ensure `app/static/js/chart.js` correctly processes the `predictions` data.

### Test the `/predict` API
1. **Using Postman**:
   - Log in via the browser (`http://localhost:5000/login`) with `testuser` and `testpass`.
   - Open browser developer tools (F12 → Application → Cookies) and copy the `session` cookie.
   - Open Postman and configure the request:
     - **URL**: `http://localhost:5000/predict`
     - **Method**: POST
     - **Headers**:
       - `Content-Type: multipart/form-data`
       - `Cookie: session=<your-session-cookie>`
     - **Body**:
       - Add a `file` field, select `test.txt`.
     - Send the request.
     - **Expected Response**: `{"result": "Normal"}`
   - Repeat with `test_malicious.txt`.
     - **Expected Response**: `{"result": "Malicious"}`

### Test Edge Cases
1. **Invalid File Upload**:
   - Upload a non-`.txt` file (e.g., `test.jpg`) via `/upload`.
   - **Expected**: Flash message: "Invalid file".

2. **Malformed File**:
   - Create a file named `bad.txt` with an incorrect format (e.g., fewer columns):
     ```
     0,tcp,http
     ```
   - Upload `bad.txt` via `/upload`.
   - **Expected**: Flash message: "Error processing file: Expected 42 columns".

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request with a description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **NSL-KDD Dataset**: Thanks to the creators for providing a valuable dataset for intrusion detection research ([NSL-KDD website](https://www.unb.ca/cic/datasets/nsl.html)).
- **Flask and Scikit-learn Communities**: For their excellent tools and documentation that made this project possible.