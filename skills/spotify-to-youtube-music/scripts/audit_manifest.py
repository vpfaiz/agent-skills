#!/usr/bin/env python3
"""Audit UI-derived source coverage, ordered IDs, and duplicate occurrences."""
import argparse
from collections import Counter
import json
from pathlib import Path


def audit(manifest):
    playlists = manifest.get('playlists') if isinstance(manifest, dict) else None
    if not isinstance(playlists, list) or not playlists:
        return {'verified': False, 'errors': ['playlists must be a nonempty list']}
    reports = []
    for playlist in playlists:
        errors = []
        if not isinstance(playlist, dict):
            reports.append({'verified': False, 'errors': ['playlist must be an object']})
            continue
        source = playlist.get('source_entries')
        destination = playlist.get('destination_entries')
        count = playlist.get('source_count')
        if not isinstance(source, list) or not isinstance(destination, list):
            reports.append({'name': playlist.get('name'), 'verified': False,
                            'errors': ['source_entries and destination_entries must be lists']})
            continue
        if type(count) is not int or count < 0 or len(source) != count:
            errors.append('source_count does not reconcile with source_entries')
        positions = [r.get('position') if isinstance(r, dict) else None for r in source]
        if type(count) is int and count >= 0 and positions != list(range(1, count + 1)):
            errors.append('source positions must cover 1..source_count in order')
        desired, statuses = [], Counter()
        for row in source:
            if not isinstance(row, dict):
                errors.append('source entry must be an object')
                continue
            status = row.get('status')
            if status not in ('matched', 'unresolved', 'unavailable'):
                errors.append(f"invalid status at position {row.get('position')}")
                continue
            statuses[status] += 1
            if status == 'matched':
                identifier = row.get('video_id')
                if not isinstance(identifier, str) or not identifier.strip():
                    errors.append(f"missing video_id at position {row.get('position')}")
                else:
                    desired.append(identifier)
                if not row.get('evidence'):
                    errors.append(f"missing match evidence at position {row.get('position')}")
            elif not row.get('reason'):
                errors.append(f"missing skip reason at position {row.get('position')}")
        actual = []
        for row in destination:
            identifier = row.get('video_id') if isinstance(row, dict) else None
            if not isinstance(identifier, str) or not identifier.strip():
                errors.append('destination entry has missing or invalid video_id')
            else:
                actual.append(identifier)
        if desired != actual:
            errors.append('destination sequence differs from matched source occurrences')
        reports.append({'name': playlist.get('name'), 'source_count': count,
                        'copied': len(actual), 'unresolved': statuses['unresolved'],
                        'unavailable': statuses['unavailable'],
                        'missing_occurrences': dict(Counter(desired) - Counter(actual)),
                        'extra_occurrences': dict(Counter(actual) - Counter(desired)),
                        'order_verified': desired == actual,
                        'verified': not errors, 'errors': errors})
    return {'verified': all(r['verified'] for r in reports), 'playlists': reports}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        result = audit(json.loads(args.manifest.read_text()))
    except (OSError, ValueError) as error:
        result = {'verified': False, 'errors': [str(error)]}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['verified'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
