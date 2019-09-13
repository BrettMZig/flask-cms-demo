from flask import render_template, redirect, request, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login import login_required
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.urls import url_parse
from .main import app
from .models import db, Post, User
from .forms import LoginForm, NewPostForm, AddUserForm


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
@app.route('/', methods=['GET'])
def index():
    page_num = request.args.get('page', 1, type=int)
    pages = Post.query.order_by(Post.timestamp.desc()).paginate(
            page_num, app.config["POSTS_PER_PAGE"], False)
    next_url = url_for('index', page=pages.next_num) \
        if pages.has_next else None
    prev_url = url_for('index', page=pages.prev_num) \
        if pages.has_prev else None
    return render_template('index.html', pages=pages.items, title="home",
                           next_url=next_url, prev_url=prev_url)


@app.route('/post/<string:post_slug>')
def view_post_by_slug(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template("page.html", title=post.title,
                           content=post.content, id=post.id)


@app.route('/post/<int:post_id>')
def view_post_by_id(post_id):
    post = Post.query.get(post_id)
    return render_template("page.html", title=post.title,
                           content=post.content, id=post.id)


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
@app.route('/new-user/', methods=['GET', 'POST'])
@login_required
def new_user():
    form = AddUserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        plain_text_password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("New user {} successfully added.".format(form.username.data))
        return redirect(url_for('index'))
    if form.errors:
        flash(form.errors)
    return render_template('new-user.html', title="Add New User", form=form)


@app.route('/new-post/', methods=['GET', 'POST'])
@login_required
def new_page():
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data,
                        content=form.content.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('view_post_by_id', post_id=new_post.id))
    if form.errors:
        flash(form.errors)
    return render_template('new-blog-post.html',
                           title="New Blog Post", form=form)


@app.route('/edit-post/<int:page_id>', methods=['GET', 'POST'])
def edit_page(page_id):
    post = db.session.query(Post).filter_by(id=page_id).first()
    form = NewPostForm(obj=post)
    if form.validate_on_submit():
        db.session.query(Post).filter_by(id=page_id).update(
            {'title': form.title.data,
             'content': form.content.data}
            )
        db.session.commit()
        return redirect(url_for('view_post_by_id', post_id=post.id))
    if form.errors:
        flash(form.errors)
    return render_template('new-blog-post.html',
                           title="Edit Blog Post", form=form)


# ---------------------------------------- #
# -- No View, Always Redirect ------------ #
# ---------------------------------------- #
# -- Pages that always redirect ----------------------------------------------#
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete-post/<int:post_id>')
@login_required
def delete_page(post_id):
    db.session.query(Post).filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/')


# ---------------------------------------- #
# -- add Admin Views --------------------- #
# ---------------------------------------- #
class SecuredModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class SecuredAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


admin = Admin(app, index_view=SecuredAdminIndexView())
admin.add_view(SecuredModelView(Post, db.session))
admin.add_view(SecuredModelView(User, db.session))
