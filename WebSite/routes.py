from flask import render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
import requests
import json
import os
from app import app

def load_verifiers():
    with open('config.json') as f:
        config = json.load(f)
        return config['verifiers']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = {
                "name": request.form['full_name'],
                "email": request.form['email'],
                "phone_number": request.form['phone']
            }

            # Check if user exists first
            user_info_response = requests.post(
                f"{app.config['API_BASE_URL']}/user-info",
                json={"phone_number": data['phone_number'], "email": data['email']}
            )

            if user_info_response.status_code == 200:
                user_data = user_info_response.json()
                if user_data.get('exists'):
                    flash('User already registered. Please login.', 'warning')
                    return redirect(url_for('login'))

            # Make API request to register user
            response = requests.post(f"{app.config['API_BASE_URL']}/register", json=data)
            if response.status_code == 200 and response.json().get('success'):
                # Request token for the user
                token_response = requests.post(
                    f"{app.config['API_BASE_URL']}/issue-token",
                    json={"phone_number": data['phone_number']}
                )

                if token_response.status_code == 200:
                    session['token_id'] = token_response.json()['token_id']
                    return redirect(url_for('dashboard'))

            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')

        except Exception as e:
            flash('Registration failed. Please try again.', 'error')
            app.logger.error(f"Registration error: {str(e)}")
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = {
                "phone_number": request.form['phone'],
                "email": request.form['email']
            }

            # Get user info from API
            response = requests.post(f"{app.config['API_BASE_URL']}/user-info", json=data)

            if response.status_code == 200:
                user_data = response.json()
                if not user_data.get('exists'):
                    flash('User not found. Please register first.', 'error')
                    return redirect(url_for('register'))

                # Request new token only if user exists and logs in
                token_response = requests.post(
                    f"{app.config['API_BASE_URL']}/issue-token",
                    json={"phone_number": data['phone_number']}
                )

                if token_response.status_code == 200:
                    session['token_id'] = token_response.json()['token_id']
                    return redirect(url_for('dashboard'))

            flash('Invalid credentials', 'error')
        except Exception as e:
            flash('Login failed. Please try again.', 'error')
            app.logger.error(f"Login error: {str(e)}")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'token_id' not in session:
        return redirect(url_for('login'))

    token_id = session['token_id']

    # Get token info to check if it's redeemed
    try:
        response = requests.get(f"{app.config['API_BASE_URL']}/token-info/{token_id}")
        if response.status_code == 200:
            token_info = response.json()
            is_redeemed = token_info.get('is_redeemed', False)
            return render_template('dashboard.html', token_id=token_id, is_redeemed=is_redeemed)
    except Exception as e:
        flash('Error fetching token status', 'error')

    return render_template('dashboard.html', token_id=token_id, is_redeemed=False)

@app.route('/verifier', methods=['GET', 'POST'])
def verifier():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        verifiers = load_verifiers()
        for verifier in verifiers:
            if verifier['username'] == username and verifier['password'] == password:
                session['verifier'] = True
                return render_template('verifier.html', authenticated=True)
        flash('Invalid credentials', 'error')

    authenticated = session.get('verifier', False)
    return render_template('verifier.html', authenticated=authenticated)

@app.route('/verify_token', methods=['POST'])
def verify_token():
    if not session.get('verifier'):
        return jsonify({"error": "Unauthorized"}), 401

    token_id = request.json.get('token')

    try:
        # Get token info from API
        response = requests.get(f"{app.config['API_BASE_URL']}/token-info/{token_id}")

        if response.status_code == 200:
            token_data = response.json()
            # If token is valid and not redeemed, redeem it
            if token_data.get('exists') and not token_data.get('is_redeemed'):
                redeem_response = requests.post(
                    f"{app.config['API_BASE_URL']}/redeem-token",
                    json={"token_id": int(token_id)}
                )
                if redeem_response.status_code == 200:
                    return jsonify({
                        "valid": True,
                        "redeemed": True,
                        "user": {
                            "name": token_data.get('owner_name'),
                            "email": token_data.get('owner_email')
                        }
                    })
            elif token_data.get('is_redeemed'):
                return jsonify({
                    "valid": True,
                    "redeemed": True,
                    "already_redeemed": True,
                    "user": {
                        "name": token_data.get('owner_name'),
                        "email": token_data.get('owner_email')
                    }
                })
        return jsonify({"valid": False})
    except Exception as e:
        return jsonify({"error": "Error verifying token"}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))