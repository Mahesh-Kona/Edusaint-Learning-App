#!/usr/bin/env python3
"""Simple migration sanity checker for Alembic revision files.

Scans `migrations/versions/` for `revision` and `down_revision` values and reports
potential multiple-heads or files that might conflict.
"""
import re
import os
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), '..')
VERSIONS = os.path.join(ROOT, 'migrations', 'versions')


def parse_file(path):
    rev = None
    down = None
    with open(path, 'r', encoding='utf8') as fh:
        for line in fh:
            if rev is None:
                m = re.match(r"^revision\s*=\s*['\"]([0-9a-fA-F]+)['\"]", line)
                if m:
                    rev = m.group(1)
            if down is None:
                m = re.match(r"^down_revision\s*=\s*(['\"])(.+?)\1", line)
                if m:
                    down = m.group(2)
            if rev and down is not None:
                break
    return rev, down


def main():
    if not os.path.isdir(VERSIONS):
        print('No migrations/versions directory found at', VERSIONS)
        return
    files = [os.path.join(VERSIONS, f) for f in os.listdir(VERSIONS) if f.endswith('.py')]
    rev_map = {}
    down_map = defaultdict(list)
    for fp in files:
        rev, down = parse_file(fp)
        name = os.path.basename(fp)
        rev_map[rev] = name
        down_map[down].append(rev)

    print('Found', len(files), 'migration files')
    heads = []
    # heads are revisions that are not referenced as down_revision by any other
    referenced = set()
    for down, revs in down_map.items():
        for r in revs:
            referenced.add(r)
    for rev in rev_map.keys():
        if rev not in referenced:
            heads.append(rev)

    print('\nRevisions by file:')
    for rev, name in rev_map.items():
        print(rev, '->', name)

    print('\nDown-revision groups:')
    for down, revs in down_map.items():
        print('down_revision=', down, 'has', len(revs), 'child(ren):', revs)

    if len(heads) > 1:
        print('\nWARNING: Multiple head revisions detected:', heads)
        print('This can cause Alembic to complain about multiple heads. Consider creating a merge migration or removing duplicate revisions if intentional.')
    else:
        print('\nNo multiple-heads detected; single head:', heads)


if __name__ == '__main__':
    main()
