"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home():
    with app.app_context():
        return redirect('/users')
    
@app.route('/users')
def users_page():
    with app.app_context():
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_page(user_id):
    with app.app_context():
        user = User.query.get_or_404(user_id)
        return render_template('user.html', user=user)
    
@app.route('/users/new')
def create_user_page():
    return render_template('create-user.html')

@app.route('/users/new', methods=['POST'])
def update_new_user():
    with app.app_context():
        #creates new User instance
        new_user = User(first_name=request.form.get('first_name'),
                         last_name=request.form.get('last_name'), 
                         image_url=request.form['image_url'] or None)
        #adds new user to db and comits it
        db.session.add(new_user)
        db.session.commit()
        #redirects to users page
        return redirect('/users')
    
@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    with app.app_context():
        user = User.query.get_or_404(user_id)
        return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        # Update user with form data
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url', 'default-profile.jpg')
        # Commit the changes
        db.session.commit()
        # Redirect to the user page
        return redirect(f'/users/{user_id}')
    
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')