from flask import render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from flask_babel import _
from app.models import Comment, Post, User, Category
from app.services import BlogService
from app.utils import paginate
from app.utils.decorators import admin_required, mod_required
from . import admin_bp
from .forms import IDVerificationForm, CreateCategoryForm, EditCategoryForm


@admin_bp.route('/moderator-dashboard')
@login_required
@mod_required
def moderator_dashboard():
  post_count = Post.query.count()
  user_count = User.query.count()
  comment_count = Comment.query.count()
  return render_template(
    'admin/moderator-dashboard.html', post_count=post_count,
    comment_count=comment_count, user_count=user_count)


@admin_bp.route('/moderate-comments', methods=['GET', 'POST'])
@login_required
@mod_required
def moderate_comments():
  form = IDVerificationForm(prefix='delete-comment')
  page = request.args.get('page', 1, type=int)
  p = paginate(Comment.query, Comment, page)

  if form.validate_on_submit():
    srv = BlogService
    comment = Comment.query.get_or_404(form.id.data)
    try:
      srv.delete_comment(comment)
      flash(_('Comment Deleted'), category='warning')
      return redirect(url_for('admin.moderate_comments', page=page))
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')

  return render_template(
    'admin/list-comments.html', form=form, 
    pagination=p['pagination'], comments=p['items'])


@admin_bp.route('/moderate-posts', methods=['GET', 'POST'])
@login_required
@mod_required
def moderate_posts():
  form = IDVerificationForm(prefix='delete-post')
  page = request.args.get('page', 1, type=int)
  p = paginate(Post.query, Post, page)
  
  if form.validate_on_submit():
    srv = BlogService
    post = Post.query.get_or_404(form.id.data)
    try:
      srv.delete_post(post)
      flash(_('Post Deleted'), category='warning')
      return redirect(url_for('admin.moderate_posts', page=page))
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')
  
  return render_template(
    'admin/list-posts.html', form=form,
    pagination=p['pagination'], posts=p['items'])


@admin_bp.route('/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
  return render_template('admin/admin-dashboard.html')


def create_category(form):
  if form.validate():
    srv = BlogService
    try:
      srv.create_category(name=form.name.data)
      flash(_('Category Created'), category='success')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')
  else:
    flash(_('Category name cannot be empty'))


def delete_cateory(form):
  if form.validate():
    srv = BlogService
    category = Category.query.get_or_404(form.id.data)
    try:
      srv.delete_cateory(category)
      flash(_('Category Deleted'), category='success')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')
  else:
    flash(_('Form validation failed'), category='warning')


def edit_category(form):
  if form.validate():
    srv = BlogService
    category = Category.query.get_or_404(form.id.data)
    try:
      srv.edit_category(category, name=form.name.data)
      flash(_('Category Edited'), category='success')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')
  else:
    flash(_('Form validation failed'), category='warning')


@admin_bp.route('/manage-categories', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_categories():
  categories = Category.query.all()
  create_category_form = CreateCategoryForm(prefix='create-category')
  delete_category_form = IDVerificationForm(prefix='delete-category')
  edit_category_form = EditCategoryForm(prefix='edit-category')
  
  if request.method == 'POST':
    if create_category_form.submit.data:
      create_category(create_category_form)
    if delete_category_form.submit.data:
      delete_cateory(delete_category_form)
    if edit_category_form.submit.data:
      edit_category(edit_category_form)
    return redirect(url_for('admin.manage_categories'))
  
  return render_template(
    'admin/manage-categories.html',
    categories=categories,
    create_category_form=create_category_form,
    delete_category_form=delete_category_form,
    edit_category_form=edit_category_form)

