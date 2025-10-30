#!/usr/bin/env python3
"""Backfill missing Asset rows for files under the uploads/ directory.

Usage:
  python scripts/backfill_assets.py [--dry-run] [--uploads PATH] [--commit]

By default runs in dry-run mode and only lists missing assets. Use --commit to insert rows.
"""
import os
import argparse
import mimetypes

from app import create_app


def find_files(root):
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            yield os.path.join(dirpath, fn)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', default=True, dest='dry_run', help='Don\'t modify the DB; just print what would be done')
    parser.add_argument('--no-dry-run', action='store_false', dest='dry_run', help='Actually write to DB')
    parser.add_argument('--uploads', type=str, default=None, help='Path to uploads directory (overrides config)')
    parser.add_argument('--commit', action='store_true', help='Alias for --no-dry-run')
    args = parser.parse_args()
    if args.commit:
        args.dry_run = False

    app = create_app()
    with app.app_context():
        UP = args.uploads or app.config.get('UPLOAD_PATH') or os.path.join(app.root_path, 'uploads')
        if not os.path.isabs(UP):
            UP = os.path.join(app.root_path, UP)
        print('Using uploads path:', UP)
        if not os.path.exists(UP):
            print('Uploads directory does not exist; nothing to do.')
            return

        from app.models import Asset
        from app.extensions import db

        missing = []
        for fp in find_files(UP):
            rel = os.path.relpath(fp, UP).replace('\\', '/')
            url = f"/uploads/{rel}"
            exists = Asset.query.filter_by(url=url).first()
            if exists:
                continue
            size = None
            try:
                size = os.path.getsize(fp)
            except Exception:
                pass
            mime_type, _ = mimetypes.guess_type(fp)
            missing.append({'path': fp, 'url': url, 'size': size, 'mime_type': mime_type})

        if not missing:
            print('No missing assets found.')
            return

        print(f'Found {len(missing)} files missing Asset rows:')
        for m in missing:
            print('-', m['url'], 'size=', m['size'], 'mime=', m['mime_type'])

        if args.dry_run:
            print('\nDry-run mode; no DB changes made. Re-run with --no-dry-run or --commit to insert rows.')
            return

        # Insert missing rows
        created = 0
        for m in missing:
            try:
                a = Asset(url=m['url'], size=m['size'], mime_type=m['mime_type'])
                db.session.add(a)
                db.session.flush()
                created += 1
            except Exception as e:
                print('Failed to insert', m['url'], '->', e)
                db.session.rollback()
        try:
            db.session.commit()
        except Exception as e:
            print('Commit failed:', e)
            db.session.rollback()
        print('Inserted', created, 'asset rows.')


if __name__ == '__main__':
    main()
