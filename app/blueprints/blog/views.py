from flask import render_template, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from flask_babel import _
from app.models import Permission
from app.services import BlogService
from app.utils.decorators import permission_required
from . import blog_bp
from .forms import CreateBlogForm


@blog_bp.route('/')
@login_required
@permission_required(Permission.WRITE)
def index():
  if current_user.blog is None:
    return redirect(url_for('blog.blank'))
  return redirect(url_for('blog.workspace'))


@blog_bp.route('/blank')
@login_required
@permission_required(Permission.WRITE)
def blank():
  if current_user.blog is not None:
    return redirect(url_for('main.index'))
  return render_template('blog/blank.html')


@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE)
def create():
  if current_user.blog is not None:
    return redirect(url_for('main.index'))
  form = CreateBlogForm()
  srv = BlogService
  if form.validate_on_submit():
    try:
      srv.create_blog(
        name=form.name.data,
        description=form.description.data,
        user=current_user._get_current_object())
      return redirect(url_for('blog.workspace'))
    except ValueError as e:
      form.name.errors.append(e)
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')
  return render_template('blog/create-blog.html', form=form)


@blog_bp.route('/workspace')
@login_required
@permission_required(Permission.WRITE)
def workspace():
  if current_user.blog is None:
    return redirect(url_for('blog.blank'))
  return render_template('blog/workspace.html')
