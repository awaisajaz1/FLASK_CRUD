from flask import render_template, url_for, redirect, flash, request, abort,Blueprint
from crud_ops.models import Post
from flask_login import current_user
from datetime import datetime, timedelta

main = Blueprint('main', __name__)


@main.route('/home', methods=['GET'])
def home():
    try:
        page = request.args.get('page', 1, type=int)
        # posts = Post.query.order_by('date_posted').filter_by(user_id=current_user.id).all()
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
        return render_template('home.html', posts=posts)
    except:
        return render_template('home.html')