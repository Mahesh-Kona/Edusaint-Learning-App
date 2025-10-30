from flask import Blueprint, render_template, render_template_string, request, redirect, url_for, session, flash, current_app
from app.extensions import db
from app.models import User
import os

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET'])
def admin_login_get():
    # Render the admin login page
    # Render the main index page which contains the login form. User requested only index.html remain.
    return render_template('index.html')


@admin_bp.route('/login', methods=['POST'])
def admin_login_post():
    # Simple session-based admin login for the admin UI
    email = request.form.get('email') or request.form.get('username')
    password = request.form.get('password')
    if not email or not password:
        flash('Missing credentials', 'error')
        return redirect(url_for('admin_bp.admin_login_get'))

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password) or user.role != 'admin':
        flash('Invalid admin credentials', 'error')
        return redirect(url_for('admin_bp.admin_login_get'))

    # success
    session['admin_user_id'] = user.id
    flash('Welcome, admin!', 'success')
    return redirect(url_for('admin_bp.admin_dashboard'))


@admin_bp.route('/dashboard')
def admin_dashboard():
    uid = session.get('admin_user_id')
    if not uid:
        return redirect(url_for('admin_bp.admin_login_get'))

    user = User.query.get(uid)
    if not user or user.role != 'admin':
        session.pop('admin_user_id', None)
        return redirect(url_for('admin_bp.admin_login_get'))

    # Prefer package template. If missing, try to read top-level templates and render via Jinja so
    # any `{{ url_for(...) }}` in the file are evaluated.
    try:
        return render_template('admin-dashboard.html', user=user)
    except Exception:
        # try reading from project-level templates/admin-dashboard.html
        # current_app.root_path -> .../flask-learning-backend/app
        project_root = os.path.abspath(os.path.join(current_app.root_path, '..'))
        candidates = [
            os.path.join(project_root, 'templates', 'admin-dashboard.html'),
            os.path.join(project_root, 'templates', 'admin-dashboard.html')
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf8') as fh:
                        content = fh.read()
                    return render_template_string(content, user=user)
                except Exception:
                    continue
        # final fallback
        return render_template('admin_dashboard_missing.html', user=user)


@admin_bp.route('/logout')
def admin_logout():
    session.pop('admin_user_id', None)
    flash('Logged out', 'info')
    # redirect to the site root (home endpoint)
    return redirect(url_for('home'))
