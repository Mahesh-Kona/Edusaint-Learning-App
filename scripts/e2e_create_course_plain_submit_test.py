import io, json
from app import create_app, db
from app.models import Course, Asset

app = create_app()
app.testing = True

png_bytes = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!'\xbc\x00\x00\x00\x00IEND\xaeB`\x82"
)

with app.test_client() as c:
    # set dev admin in session
    with c.session_transaction() as sess:
        sess['admin_user_id'] = 'dev_admin'

    # Build multipart data to simulate plain form submit including file
    data = {
        'title': 'PlainSubmit Course',
        'description': 'plain form submit test',
        'category': 'science',
        'class': '10',
        'price': '1999',
        'duration': '8',
        'weekly_hours': '4',
        'stream': 'science',
        'difficulty': 'intermediate',
        'tags': 'cbse,math',
        'published': 'on',
        'featured': 'on'
    }
    data_files = {
        'thumbnail': (io.BytesIO(png_bytes), 'plain.png')
    }

    resp = c.post('/admin/create_course', data={**data, **data_files}, content_type='multipart/form-data', headers={'X-Requested-With':'XMLHttpRequest'})
    print('STATUS', resp.status_code)
    try:
        print('JSON:', resp.get_json())
    except Exception:
        print('No JSON')

    with app.app_context():
        course = Course.query.filter_by(title='PlainSubmit Course').order_by(Course.created_at.desc()).first()
        if course:
            print('COURSE:', course.id, course.title, course.thumbnail_url, course.thumbnail_asset_id, course.category, course.class_name, course.price, course.duration_weeks, course.weekly_hours, course.stream, course.published, course.featured)
        else:
            print('Course not found')

print('done')
