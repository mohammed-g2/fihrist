from flask import render_template
from flask_login import login_required
from . import user_bp


@user_bp.route('/settings')
@login_required
def settings():
  return render_template('user/settings.html')
