from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy credentials for login
USER_CREDENTIALS = {
    'admin': 'password123'
}

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['user'] = username  # Store username in session
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

# Route for file upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user' not in session:  # Ensure user is logged in
        flash('Please log in first')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Save file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash(f'File "{file.filename}" uploaded successfully!')
    
    return render_template('upload.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear session
    flash('You have been logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
