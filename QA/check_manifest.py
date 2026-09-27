"""Validate spread manifest structure without granting visual or author approval."""
import argparse
from pathlib import Path
import sys
import yaml
from check_canon import read_yaml


def validate_manifest(data):
    errors = []
    for key in ('spread', 'status', 'version_b'):
        if key not in data:
            errors.append(f'missing {key}')
    for key in ('spread', 'status'):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            errors.append(f'{key}: expected nonempty text')
    for key in ('version_a', 'version_b'):
        if key not in data:
            continue
        record = data[key]
        if not isinstance(record, dict):
            errors.append(f'{key}: expected a mapping')
            continue
        for field in ('status', 'path'):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f'{key}.{field}: expected nonempty text')
        raw_path = record.get('path')
        if isinstance(raw_path, str):
            path = Path(raw_path)
            if path.is_absolute() or '..' in path.parts:
                errors.append(f'{key}.path: must stay within the spread folder')
    if 'final_locked' in data and type(data['final_locked']) is not bool:
        errors.append('final_locked: expected a boolean')
    if data.get('final_locked') is True or str(data.get('status')).replace('_', ' ').upper() == 'FINAL LOCKED':
        if not isinstance(data.get('approved_by'), str) or not data['approved_by'].strip():
            errors.append('locked manifest requires an explicit approved_by record; automation cannot supply approval')
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args(argv)
    try:
        errors = validate_manifest(read_yaml(args.manifest))
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        errors = [str(exc)]
    print('FAIL manifest: ' + '; '.join(errors) if errors else 'PASS manifest structure (not visual or author approval)')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
