from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from crud_ops.posts.forms import PostForm
from crud_ops.users.forms import LoginForm
from crud_ops.models import Post, User
from crud_ops import  db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta

posts = Blueprint('posts', __name__)



@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            return e
        flash('Your Post has been submitted!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/singlepost/<int:post_id>', methods=['GET', 'POST'])
def singlepost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('singlepost.html', post=post)


@posts.route('/singlepost/<int:post_id>/update',methods=['GET', 'POST'] )
@login_required
def update_singlepost(post_id):
    post = Post.query.get_or_404(post_id)
    if str(post.user_id) != str(current_user.id):
        return abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated successfully!','success')
        return redirect(url_for('posts.singlepost', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', title='Update Post', form=form, legend='Update Post') 




@posts.route('/singlepost/<int:post_id>/delete',methods=['GET', 'POST'] )
@login_required
def delete_singlepost(post_id):
    post = Post.query.get_or_404(post_id)
    if str(post.user_id) != str(current_user.id):
        return abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))