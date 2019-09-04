from flask import render_template, redirect, request, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from .main import app
from .models import db, Post, User
from .forms import LoginForm

login = LoginManager(app)
login.login_view = 'login'  # where to go when not logged in
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# -- Error Pages ------------------------- #
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# ---------------------------------------- #
# -- No Login Required Pages ------------- #
# ---------------------------------------- #
@app.route('/')
def index():
    pages = Post.query.all()
    return render_template('index.html', pages=pages, title="home")


@app.route('/post/<string:post_slug>')
def view_post_by_slug(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template("page.html", title=post.title, content=post.content, id = post.id)


@app.route('/post/<int:post_id>')
def view_post_by_id(post_id):
    post = Post.query.get(post_id)
    return render_template("page.html", title=post.title, content=post.content, id = post.id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# ---------------------------------------- #
# -- Login Required Pages to View -------- #
# ---------------------------------------- #
@app.route('/new-post/')
@login_required
def new_page():
    return render_template('new-page.html')


@app.route('/edit-post/<int:page_id>')
def edit_page(page_id):
    page = db.session.query(Post).filter_by(id=page_id).first()
    return render_template('edit-post.html',
                           id=page.id, title=page.title, content=page.content)


# ---------------------------------------- #
# -- No View, Always Redirect ------------ #
# ---------------------------------------- #
# -- Pages that always redirect ----------------------------------------------#
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/save-post/', methods=['POST'])
@login_required
def save_page():
    page = Post(title=request.form['title'],
                content=request.form['content'])
    db.session.add(page)
    db.session.commit()
    return redirect('/post/%d' % page.id)


@app.route('/update-post/', methods=['POST'])
@login_required
def update_page():
    page_id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    db.session.query(Post).filter_by(id=page_id).update(
            {'title': title, 'content': content}
            )
    db.session.commit()
    return redirect('/post/'+page_id)


@app.route('/delete-post/<int:post_id>')
@login_required
def delete_page(post_id):
    db.session.query(Post).filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/')
