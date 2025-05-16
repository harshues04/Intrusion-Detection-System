from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource
from app import db
from app.models import User, Prediction
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

def init_routes(app, api):
    model = joblib.load('model/svm_model.pkl')
    scaler = joblib.load('model/scaler.pkl')
    encoders = {
        'protocol_type': joblib.load('model/protocol_type_encoder.pkl'),
        'service': joblib.load('model/service_encoder.pkl'),
        'flag': joblib.load('model/flag_encoder.pkl')
    }

    columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
        'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
        'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
        'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
        'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
        'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
    ]

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('upload'))
            flash('Invalid credentials')
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('Username exists')
            else:
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash('Signup successful')
                return redirect(url_for('login'))
        return render_template('signup.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        if request.method == 'POST':
            file = request.files['file']
            if file and file.filename.endswith('.txt'):
                df = pd.read_csv(file, sep=',', names=columns + ['class', 'extra'], header=None)
                df = df.drop(['class', 'extra'], axis=1)
                for col in ['protocol_type', 'service', 'flag']:
                    df[col] = encoders[col].transform(df[col])
                X = scaler.transform(df)
                predictions = model.predict(X)
                result = 'Malicious' if predictions[0] == 1 else 'Normal'
                pred = Prediction(user_id=current_user.id, filename=file.filename, result=result)
                db.session.add(pred)
                db.session.commit()
                return redirect(url_for('dashboard'))
            flash('Invalid file')
        return render_template('upload.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        predictions = Prediction.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', predictions=predictions)

    class PredictAPI(Resource):
        @login_required
        def post(self):
            file = request.files['file']
            if file and file.filename.endswith('.txt'):
                df = pd.read_csv(file, sep=',', names=columns + ['class', 'extra'], header=None)
                df = df.drop(['class', 'extra'], axis=1)
                for col in ['protocol_type', 'service', 'flag']:
                    df[col] = encoders[col].transform(df[col])
                X = scaler.transform(df)
                predictions = model.predict(X)
                return {'result': 'Malicious' if predictions[0] == 1 else 'Normal'}, 200
            return {'error': 'Invalid file'}, 400

    api.add_resource(PredictAPI, '/predict')