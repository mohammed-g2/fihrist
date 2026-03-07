from flask import render_template, redirect, url_for, request, session
from . import main_bp


@main_bp.route('/')
def index():
  return render_template('index.html')


@main_bp.route('/<lang>')
def set_language(lang):
  session['LANGUAGE'] = lang
  print('*' * 10, lang, '*' * 10)
  print('*' * 10, session['LANGUAGE'], '*' * 10)
  url = request.args.get('next')
  if not url.startswith('/'):
    url = url_for('main.index')

  return redirect(url)
