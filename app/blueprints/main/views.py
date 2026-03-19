from flask import render_template, redirect, url_for, request, session
from app.models import Post, Category
from app.utils import paginate
from . import main_bp


@main_bp.route('/')
def index():
  page = request.args.get('page', 1, type=int)
  p = paginate(Post.query.filter_by(status='published'), Post, page)
  categories = Category.query.all()
  endpoint = 'main.index'
  return render_template(
    'index.html', posts=p['items'], pagination=p['pagination'],
    categories=categories, endpoint=endpoint)


@main_bp.route('/<slug>')
def get_by_category(slug):
  page = request.args.get('page', 1, type=int)
  category = Category.query.filter_by(slug=slug).first_or_404()
  p = paginate(Post.query.filter_by(category=category, status='published'), Post, page)
  categories = Category.query.all()
  endpoint = 'main.get_by_category'
  return render_template(
    'index.html', posts=p['items'], pagination=p['pagination'],
    categories=categories, endpoint=endpoint, current_category=category)


@main_bp.route('/translate/<lang>')
def set_language(lang):
  session['LANGUAGE'] = lang
  url = request.args.get('next')
  if url and not url.startswith('/'):
    url = url_for('main.index')
  else:
    url = '/'

  return redirect(url)
