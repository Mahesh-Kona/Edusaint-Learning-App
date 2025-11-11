import io
from app import create_app
from app.models import Course, Asset

app = create_app()
app.testing = True

png_bytes = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!'\xbc\x00\x00\x00\x00IEND\xaeB`\x82"
)

with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['admin_user_id'] = 'dev_admin'

    # upload first
    data = { 'file': (io.BytesIO(png_bytes), 'jsflow.png') }
    up = c.post('/api/v1/uploads', data=data, content_type='multipart/form-data')
    print('upload status', up.status_code, 'json=', up.get_json())
    uj = up.get_json() or {}
    asset_id = uj.get('asset_id')
    url = uj.get('url')

    # now send the course create as XHR with all fields (simulate the JS)
    form = {
        'title': 'JS Flow Course',
        'description': 'created via simulated js flow',
        'category': 'mathematics',
        'class': '11',
        'price': '2499',
        'duration': '10',
        'weekly_hours': '6',
        'difficulty': 'advanced',
        'stream': 'science',
        'tags': 'cbse,advanced',
        'published': 'on',
        'featured': 'on'
    }
    if asset_id:
        form['thumbnail_asset_id'] = str(asset_id)
    if url:
        form['thumbnail_url'] = url

    resp = c.post('/admin/create_course', data=form, headers={'X-Requested-With':'XMLHttpRequest'})
    print('create status', resp.status_code, 'json=', resp.get_json())

    with app.app_context():
        cobj = Course.query.filter_by(title='JS Flow Course').order_by(Course.created_at.desc()).first()
        aobj = Asset.query.filter_by(url=url).order_by(Asset.created_at.desc()).first()
        print('DB course:', cobj and {'id':cobj.id,'thumbnail_asset_id':cobj.thumbnail_asset_id,'thumbnail_url':cobj.thumbnail_url,'duration_weeks':cobj.duration_weeks,'weekly_hours':cobj.weekly_hours,'difficulty':cobj.difficulty,'stream':cobj.stream,'tags':cobj.tags,'published':cobj.published,'featured':cobj.featured} )
        print('DB asset:', aobj and {'id':aobj.id,'url':aobj.url})

print('done')
