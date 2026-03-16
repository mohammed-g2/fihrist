from flask import render_template, redirect, url_for, request, session
from app.models import Post
from app.utils import paginate
from . import main_bp


@main_bp.route('/')
def index():
  page = request.args.get('page', 1, type=int)
  p = paginate(Post.query, Post, page)
  return render_template(
    'index.html', posts=p['items'], pagination=p['pagination'])


@main_bp.route('/translate/<lang>')
def set_language(lang):
  session['LANGUAGE'] = lang
  url = request.args.get('next')
  if url and not url.startswith('/'):
    url = url_for('main.index')
  else:
    url = '/'

  return redirect(url)
