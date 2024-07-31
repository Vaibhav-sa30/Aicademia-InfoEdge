from flask import Flask, request, jsonify, render_template, redirect, session, url_for, flash
from flask_cors import CORS
import pandas as pd
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aicademia.db'
app.config['SECRET_KEY'] = 'vaibhav@aicademia'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        user = User.query.filter(
            (User.email == username_or_email) | (User.username == username_or_email)
        ).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            if user.is_student:
                return redirect(url_for('student_dashboard'))
            elif user.is_professional:
                return redirect(url_for('professional_dashboard'))
            elif user.is_business:
                return redirect(url_for('business_dashboard'))
            else:
                flash("Invalid user role.", "error")
        else:
            flash("Invalid credentials. Please try again.", "error")
        
    return render_template('user_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cnf_password = request.form['cnf-password']

        if password != cnf_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please login.", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please login.", "success")
        return redirect(url_for('user_login'))

    return render_template('registration.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    # Process the file here
    return jsonify({'message': 'File uploaded successfully'})

def check_bias(data, label, protected_attr, favorable_class, privileged_value):
    try:
        # Ensure privileged_value is formatted correctly
        privileged_classes = [[privileged_value]]

        # Create the dataset
        dataset = StandardDataset(
            df=data,
            label_name=label,
            favorable_classes=[favorable_class],
            protected_attribute_names=[protected_attr],
            privileged_classes=privileged_classes
        )

        # Define the metric
        metric = BinaryLabelDatasetMetric(
            dataset,
            privileged_groups=[{protected_attr: privileged_value}],
            unprivileged_groups=[{protected_attr: lambda x: x != privileged_value}]
        )

        # Return the bias metrics
        bias_metrics = {
            'mean_difference': metric.mean_difference(),
            'disparate_impact': metric.disparate_impact()
        }
        return bias_metrics
    except Exception as e:
        print("Error in check_bias function:", e)
        raise

@app.route('/check-bias', methods=['POST'])
def check_bias_route():
    try:
        print("Request received")
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        print("File received:", file.filename)
        data = pd.read_csv(file)
        print("Data read into dataframe")

        label = request.form['label']
        print("Label received:", label)

        protected_attr = request.form['protected_attr']
        print("Protected attribute received:", protected_attr)

        favorable_class = request.form['favorable_class']
        print("Favorable class received:", favorable_class)

        privileged_value = request.form['privileged_value']
        print("Privileged value received:", privileged_value)

        bias_metrics = check_bias(data, label, protected_attr, favorable_class, privileged_value)
        print("Bias metrics calculated:", bias_metrics)

        return jsonify(bias_metrics)
    except Exception as e:
        print("Error processing request:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
