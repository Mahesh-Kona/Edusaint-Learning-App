import sys, os
# ensure project root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.extensions import db

app = create_app()
app.config.update({
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "SQLALCHEMY_ENGINE_OPTIONS": {},
})
with app.app_context():
    db.create_all()
    client = app.test_client()
    rv = client.post('/api/v1/auth/register', json={'email':'u1@example.com','password':'secret','role':'teacher'})
    print('register', rv.status_code, rv.get_json())
    rv2 = client.post('/api/v1/auth/login', json={'email':'u1@example.com','password':'secret'})
    print('login', rv2.status_code, rv2.get_json())
    refresh = rv2.get_json().get('refresh_token')
    headers = {'Authorization': f'Bearer {refresh}'}
    rv3 = client.post('/api/v1/auth/refresh', headers=headers)
    print('refresh status', rv3.status_code)
    print('refresh json', rv3.get_data(as_text=True))
