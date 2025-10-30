import io
import os
import tempfile

def test_upload_local_file(client, tmp_path):
    # Ensure upload path is a temp dir for test isolation
    client.application.config['UPLOAD_PATH'] = str(tmp_path)

    data = {
        'file': (io.BytesIO(b'hello world'), 'test.png')
    }
    rv = client.post('/api/v1/uploads', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200
    js = rv.get_json()
    assert js['success'] is True
    assert 'url' in js and js['mime_type'] in ('image/png', 'image/octet-stream', 'image/jpeg') or js['mime_type']
    # check file saved
    saved = os.path.join(client.application.config['UPLOAD_PATH'], 'test.png')
    assert os.path.exists(saved)
