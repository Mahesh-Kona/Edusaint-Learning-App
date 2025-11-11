import io, json
from app import create_app, db
from app.models import Course, Asset

app = create_app()
app.testing = True

png_bytes = (
    b"\x89PNG\r\n\x1a\n"  # PNG header
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!'\xbc\x00\x00\x00\x00IEND\xaeB`\x82"
)

with app.test_client() as c:
    # set dev admin in session
    with c.session_transaction() as sess:
        sess['admin_user_id'] = 'dev_admin'

    # 1) Upload the image
    data = {
        'file': (io.BytesIO(png_bytes), 'test.png')
    }
    resp = c.post('/api/v1/uploads', data=data, content_type='multipart/form-data')
    print('UPLOAD status:', resp.status_code)
    try:
        upjson = resp.get_json()
    except Exception:
        upjson = None
    print('UPLOAD json:', upjson)

    asset_id = None
    url = None
    if upjson and upjson.get('asset_id'):
        asset_id = upjson.get('asset_id')
        url = upjson.get('url')

    # 2) Create the course, include returned asset id and url
    form = {
        'title': 'E2E Test Course',
        'description': 'created by automated test',
        'category': 'TestCat',
        'class': 'TestClass'
    }
    if asset_id:
        form['thumbnail_asset_id'] = str(asset_id)
    if url:
        form['thumbnail_url'] = url

    resp2 = c.post('/admin/create_course', data=form)
    print('CREATE status:', resp2.status_code)
    try:
        create_json = resp2.get_json()
    except Exception:
        create_json = None
    print('CREATE json:', create_json)

    # 3) Inspect DB for course and asset
    with app.app_context():
        course = Course.query.filter_by(title='E2E Test Course').order_by(Course.created_at.desc()).first()
        asset = None
        if url:
            asset = Asset.query.filter_by(url=url).order_by(Asset.created_at.desc()).first()
        print('DB course:', {'id': course.id if course else None, 'thumbnail_asset_id': getattr(course, 'thumbnail_asset_id', None) if course else None, 'thumbnail_url': getattr(course,'thumbnail_url', None) if course else None})
        print('DB asset:', {'id': asset.id if asset else None, 'url': asset.url if asset else None})

print('done')
