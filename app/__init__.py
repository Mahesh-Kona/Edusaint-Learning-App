from flask import Flask, jsonify, request
import os

from app.extensions import db, migrate, jwt, cors, limiter, cache
from app.routes.auth_routes import auth_bp
from app.api import bp as api_bp
from app.routes.demo_routes import bp as demo_bp
from app.routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    # Initialize limiter with storage URI if provided (Redis) and set default limits
    limiter_storage = app.config.get('RATELIMIT_STORAGE_URL')
    default_limits = app.config.get('RATELIMIT_DEFAULTS')
    limiter_kwargs = {}
    if limiter_storage:
        limiter_kwargs['storage_uri'] = limiter_storage
    # Do not pass default_limits directly to init_app (not accepted by all limiter versions)
    # Instead, expose parsed defaults in app.config for potential use.
    if default_limits:
        if isinstance(default_limits, str) and (';' in default_limits or ',' in default_limits):
            parts = [p.strip() for p in default_limits.replace(';', ',').split(',') if p.strip()]
        else:
            parts = [default_limits]
        app.config['RATELIMIT_DEFAULTS'] = parts
    limiter.init_app(app, **limiter_kwargs)
    # Initialize cache (will pick RedisCache if configured)
    cache.init_app(app)

    # Blueprints
    # API blueprint (v1 endpoints under /api/v1/... via the route definitions)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    # Auth routes are currently defined as full paths; register without prefix to keep existing routes
    app.register_blueprint(auth_bp)
    # Demo page for browser verification
    app.register_blueprint(demo_bp)
    # Admin login/dashboard
    app.register_blueprint(admin_bp)

    # Global JSON error handler
    @app.errorhandler(Exception)
    def handle_error(e):
        code = getattr(e, 'code', 500)
        return jsonify({
            "success": False,
            "error": str(e),
            "code": code
        }), code

    # Security headers and small hardening
    @app.after_request
    def set_security_headers(response):
        # Basic headers (adjust as needed in production)
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('X-Frame-Options', 'DENY')
        response.headers.setdefault('Referrer-Policy', 'no-referrer')
        response.headers.setdefault('X-XSS-Protection', '1; mode=block')
        # Add Content Security Policy header from config
        csp = app.config.get('CONTENT_SECURITY_POLICY')
        if csp:
            response.headers.setdefault('Content-Security-Policy', csp)
        return response

    @app.route('/csp-report', methods=['POST'])
    def csp_report():
        # Accept and log CSP violation reports from browsers (Content-Security-Policy-Report-Only or report-uri)
        try:
            data = request.get_json(silent=True)
            app.logger.warning('CSP report: %s', data)
            # also persist reports to a log file for later analysis
            try:
                import json
                logs_dir = os.path.join(app.instance_path, 'logs')
                os.makedirs(logs_dir, exist_ok=True)
                fp = os.path.join(logs_dir, 'csp_reports.jsonl')
                with open(fp, 'a', encoding='utf8') as fh:
                    fh.write(json.dumps({'ts': __import__('time').time(), 'report': data}) + '\n')
            except Exception:
                app.logger.exception('Failed to persist CSP report')
        except Exception:
            app.logger.exception('Failed to parse CSP report')
        return ('', 204)

    @app.route('/')
    def home():
        # Serve the admin login page at the root (index)
        try:
            # Always render the site's index.html at the root.
            # Do not redirect automatically to the admin dashboard — the user requested the
            # root URL always show the index page.
            from flask import render_template
            return render_template('index.html')
        except Exception:
            return jsonify({"message": "Flask Learning Backend is running 🚀"})

    # Serve uploaded files from UPLOAD_PATH in development
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        from flask import send_from_directory
        up = app.config.get('UPLOAD_PATH', '/tmp/uploads')
        # resolve relative upload paths relative to the application root
        try:
            if not os.path.isabs(up):
                resolved_up = os.path.join(app.root_path, up)
            else:
                resolved_up = up
            # safety: ensure the directory exists and file is present
            fp = os.path.join(resolved_up, filename)
            if not os.path.exists(fp):
                app.logger.debug('Uploaded file not found on disk: %s (resolved path: %s)', filename, fp)
                return jsonify({'success': False, 'error': 'file not found', 'code': 404}), 404
            return send_from_directory(resolved_up, filename)
        except Exception as e:
            app.logger.exception('Failed to serve uploaded file')
            return jsonify({'success': False, 'error': 'file not found', 'code': 404}), 404

    return app
