from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import boto3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

# Flask-Login Configuration
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms for user registration and login
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Function to generate presigned URL for the private image
def generate_presigned_url(bucket_name, key):
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=3600  
    )
    return url

s3 = boto3.client('s3', region_name='us-east-1') 
imgBackground = generate_presigned_url('bucketusersapp', 'usersBackground.jpg')
imgUser = generate_presigned_url('bucketusersapp', 'user.jpg')

#public image
# imgBackground_url = s3.generate_presigned_url('get_object',
#                                           Params={'Bucket': 'bucketusersapp',
#                                                  'Key': 'usersBackground.jpg'})
# imgUser_url = s3.generate_presigned_url('get_object',
#                                           Params={'Bucket': 'bucketusersapp',
#                                                  'Key': 'user.jpg'})

# Routes
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html',imgBackground=imgBackground,imgUser=imgUser,users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        
        # Check if username and email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register'))
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists. Please choose a different email.', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form,imgBackground=imgBackground)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Login failed. Incorrect password.', 'danger')
        else:
            flash('Login failed. User does not exist.', 'danger')
    return render_template('login.html', form=form,imgBackground=imgBackground)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)