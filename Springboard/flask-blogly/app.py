"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
        db.drop_all()
        db.create_all()

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
        posts = Post.query.filter(Post.user_id == user_id)
        return render_template('user.html', user=user, posts=posts)
    
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
    
@app.route('/users/<int:user_id>/posts/new')
def show_form(user_id):
    """Show form to add a post for that user."""
    with app.app_context():
        user = User.query.get_or_404(user_id)
        return render_template('add-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    with app.app_context():
        new_post = Post(title=request.form.get('title'),
                        content=request.form.get('content'),
                        user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    with app.app_context():
        post = Post.query.get(post_id)
        return render_template('show-post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_page(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    with app.app_context():
        post = Post.query.get(post_id)
        return render_template('edit-post.html', post=post)
    
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    with app.app_context():
        post = Post.query.get(post_id)
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(f'/posts/{post_id}')
    
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')
