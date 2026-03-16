from flask import render_template, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user
from flask_babel import _
from app.models import Permission, Post
from app.services import BlogService
from app.utils import paginate
from app.utils.decorators import permission_required
from . import blog_bp
from .forms import CreateBlogForm, CreatePostForm


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
  page = request.args.get('page', 1, type=int)
  p = paginate(current_user.posts, Post, page)
  return render_template(
    'blog/workspace.html', posts=p['items'], pagination=p['pagination'])


@blog_bp.route('/create-post', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE)
def create_post():
  if current_user.blog is None:
    return redirect(url_for('blog.blank'))
  
  form = CreatePostForm()
  
  if form.validate_on_submit():
    srv = BlogService
    try:
      srv.create_post(
        user=current_user._get_current_object(),
        title=form.title.data,
        content=form.content.data,
        status='draft')
      flash(_('Post Saved.'), category='success')
      return redirect(url_for('blog.workspace'))
    except ValueError:
      flash(_('Title already exists'), category='warning')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')

  return render_template('blog/create-post.html', form=form)


@blog_bp.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE)
def edit_post(id):
  post = Post.query.get_or_404(id)
  if post.user.id != current_user.id:
    return redirect(url_for('blog.index'))

  form = CreatePostForm()
  
  if form.validate_on_submit():
    srv = BlogService
    try:
      srv.update_post(post, title=form.title.data, content=form.content.data)
      flash(_('Post Updated'), category='success')
      return redirect(url_for('blog.workspace'))
    except ValueError:
      flash(_('Title already exists'), category='warning')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')
  
  form.title.data = post.title
  form.content.data = post.content
  
  return render_template('blog/edit-post.html', form=form, post=post)


@blog_bp.route('/post/<slug>')
def get_post(slug):
  post = Post.query.filter_by(slug=slug).first_or_404()
  
  return render_template('blog/post.html', post=post)
