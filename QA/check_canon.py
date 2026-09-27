"""Read-only canon reference validation; optional hashing of raw Drive downloads."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_yaml(path):
    with Path(path).open(encoding='utf-8') as stream:
        value = yaml.load(stream, Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError(f'{path}: expected a YAML mapping')
    return value


class Check:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.assets = {}
        self.verified = 0
        self.attempted = 0

    def require(self, condition, message):
        if not condition:
            self.errors.append(message)

    def mapping(self, value, label):
        if not isinstance(value, dict):
            self.errors.append(f'{label}: expected a mapping')
            return {}
        return value

    def names(self, value, label):
        if not isinstance(value, list) or not all(isinstance(n, str) for n in value):
            self.errors.append(f'{label}: expected a list of names')
            return []
        self.require(len(value) == len(set(value)), f'{label}: duplicate names')
        return value

    def asset(self, record, id_key, hash_key, label, optional_hash=False):
        record = self.mapping(record, label)
        identity, digest = record.get(id_key), record.get(hash_key)
        valid_id = isinstance(identity, str) and re.fullmatch(r'[A-Za-z0-9_-]{10,}', identity)
        self.require(valid_id, f'{label}.{id_key}: missing or invalid Drive ID')
        if digest is None and optional_hash:
            self.warnings.append(f'{label}.{hash_key}: missing; byte verification remains incomplete')
        else:
            self.require(isinstance(digest, str) and re.fullmatch(r'[0-9a-f]{64}', digest),
                         f'{label}.{hash_key}: expected lowercase SHA256 (64 hex characters)')
        if valid_id:
            prior = self.assets.get(identity)
            if prior and prior[0] is not None and digest is not None:
                self.require(prior[0] == digest, f'{label}: conflicting hashes for Drive ID {identity}')
            if prior is None or prior[0] is None:
                self.assets[identity] = (digest, label)

    def equal(self, left, right, label):
        self.require(left is not None and left == right, f'{label}: reference mismatch')


def validate(registry, rules, profiles=()):
    c = Check()
    chars = c.mapping(registry.get('characters'), 'characters')
    c.require(bool(chars), 'characters: empty registry')
    for name, raw in chars.items():
        record = c.mapping(raw, f'characters.{name}')
        c.asset(record, 'image_id', 'image_sha256', name)
        c.asset(record, 'profile_id', 'profile_sha256', name, optional_hash=True)
        if record.get('branding_authority') != 'source_image' or 'logo_id' in record:
            c.asset(record, 'logo_id', 'logo_sha256', name)
        if 'vest_back_emblem_id' in record or 'vest_back_emblem_sha256' in record:
            c.asset(record, 'vest_back_emblem_id', 'vest_back_emblem_sha256', name)
    visuals = c.mapping(registry.get('project_visuals'), 'project_visuals')
    c.require(bool(visuals), 'project_visuals: empty registry')
    for name, record in visuals.items():
        c.asset(record, 'image_id', 'sha256', f'project_visuals.{name}')
    branding = c.mapping(registry.get('branding_assets'), 'branding_assets')
    emblem = c.mapping(branding.get('circular_club_emblem'), 'circular_club_emblem')
    c.asset(emblem, 'image_id', 'sha256', 'circular_club_emblem')
    er = c.mapping(rules.get('children_vest_back_emblem'), 'children_vest_back_emblem')
    c.asset(er, 'image_id', 'sha256', 'children_vest_back_emblem')
    for key in ('image_id', 'sha256', 'asset_filename'):
        c.equal(er.get(key), emblem.get(key), f'emblem.{key}')
    wearers = c.names(er.get('characters'), 'emblem.characters')
    c.require(set(wearers) == set(c.names(emblem.get('characters'), 'registry emblem.characters')),
              'emblem: registry/rules wearer sets differ')
    for name in wearers:
        record = c.mapping(chars.get(name), name)
        c.equal(record.get('vest_back_emblem_id'), er.get('image_id'), f'{name}.emblem_id')
        c.equal(record.get('vest_back_emblem_sha256'), er.get('sha256'), f'{name}.emblem_hash')
    c.require({n for n, r in chars.items() if isinstance(r, dict) and 'vest_back_emblem_id' in r} == set(wearers),
              'emblem: character applications differ from wearer list')
    badge = c.mapping(rules.get('hard_hat_badge'), 'hard_hat_badge')
    c.asset(badge, 'logo_id', 'logo_sha256', 'hard_hat_badge')
    for name in c.names(badge.get('characters'), 'badge.characters'):
        record = c.mapping(chars.get(name), name)
        for key in ('logo_id', 'logo_sha256'):
            c.equal(record.get(key), badge.get(key), f'{name}.badge.{key}')
    variants = c.mapping(c.mapping(branding.get('civic_ridge_hard_hat_variants'), 'Civic Ridge').get('variants'), 'Civic Ridge variants')
    for name, raw in variants.items():
        record = c.mapping(raw, f'variant.{name}')
        c.asset(record, 'image_id', 'sha256', f'variant.{name}')
        char = c.mapping(chars.get(name), name)
        c.equal(char.get('logo_id'), record.get('image_id'), f'{name}.variant_id')
        c.equal(char.get('logo_sha256'), record.get('sha256'), f'{name}.variant_hash')
    sticker = c.mapping(rules.get('fire_station_project_sticker'), 'fire_station_project_sticker')
    c.asset(sticker, 'image_id', 'sha256', 'fire_station_project_sticker')
    registered = c.mapping(visuals.get('fire_station_project_sticker'), 'registered sticker')
    for key in ('image_id', 'sha256'):
        c.equal(sticker.get(key), registered.get(key), f'sticker.{key}')
    placements = c.mapping(sticker.get('placements'), 'sticker.placements')
    for name, placement in placements.items():
        c.require(name in chars, f'sticker: unknown character {name}')
        c.require(isinstance(placement, str) and bool(placement.strip()), f'{name}: missing sticker placement')
    adults = c.mapping(c.mapping(rules.get('job_sticker_cast_records'), 'job_sticker_cast_records').get('adults'), 'sticker adults')
    exclusions = set()
    for name, raw in adults.items():
        record = c.mapping(raw, name)
        char = c.mapping(chars.get(name), name)
        for key in ('profile', 'image'):
            c.equal(record.get(key+'_drive_id'), char.get(key+'_id'), f'{name}.sticker.{key}')
        if record.get('job_stickers_allowed') is False:
            exclusions.add(name)
            c.require(name not in placements and record.get('confirmed_stickers') == [], f'{name}: excluded from job stickers')
    c.require(set(placements) | exclusions == set(chars), 'sticker coverage: missing or unknown characters')
    for name, record in adults.items():
        if not isinstance(record, dict) or name in exclusions:
            continue
        confirmed = record.get('confirmed_stickers')
        if not isinstance(confirmed, list):
            c.errors.append(f'{name}: confirmed_stickers must be a list')
            continue
        for item in confirmed:
            item = c.mapping(item, f'{name}.confirmed_stickers')
            if item.get('asset_registry_key') == 'project_visuals.fire_station_project_sticker':
                c.equal(item.get('permanent_location'), placements.get(name), f'{name}.sticker placement')
    def check_links(value, label):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ('asset_registry_key', 'immutable_asset'):
                    target = registry
                    if isinstance(item, str):
                        for part in item.split('.'):
                            target = target.get(part) if isinstance(target, dict) else None
                    else:
                        target = None
                    c.require(isinstance(target, dict), f'{label}.{key}: unresolved registry reference {item}')
                check_links(item, f'{label}.{key}')
        elif isinstance(value, list):
            for index, item in enumerate(value):
                check_links(item, f'{label}[{index}]')
    check_links(rules, 'rules')
    dims = c.mapping(c.mapping(rules.get('character_dimensions_and_helmet_colors'), 'dimensions').get('characters'), 'dimension characters')
    c.require(set(dims) == set(chars), 'dimensions: character coverage differs from registry')
    for name, raw in dims.items():
        record = c.mapping(raw, name)
        h = record.get('standing_height_inches')
        c.require(type(h) in (int, float) and math.isfinite(h) and h > 0, f'{name}: invalid standing height')
        color = record.get('hard_hat_color')
        c.require((isinstance(color, str) and bool(color.strip())) or
                  (color is None and record.get('construction_ppe_allowed') is False), f'{name}: missing helmet color or explicit no-PPE rule')
        char = c.mapping(chars.get(name), name)
        for key in ('profile', 'image'):
            c.equal(record.get(key+'_drive_id'), char.get(key+'_id'), f'{name}.dimensions.{key}')
    order = c.names(rules.get('height_order'), 'height_order')
    c.require(bool(order), 'height_order: empty list')
    heights = [dims.get(n, {}).get('standing_height_inches') if isinstance(dims.get(n), dict) else None for n in order]
    if all(type(h) in (int, float) for h in heights):
        c.require(all(a > b for a, b in zip(heights, heights[1:])), 'height_order contradicts standing heights')
    else:
        c.errors.append('height_order references missing heights')
    aliases = {'master_profile_drive_id':'profile_id', 'approved_image_drive_id':'image_id',
               'master_profile_sha256':'profile_sha256', 'approved_image_sha256':'image_sha256',
               'hard_hat_badge_drive_id':'logo_id', 'hard_hat_badge_sha256':'logo_sha256',
               'vest_back_emblem_drive_id':'vest_back_emblem_id', 'vest_back_emblem_sha256':'vest_back_emblem_sha256'}
    for path, profile in profiles:
        profile = c.mapping(profile, str(path))
        name = str(profile.get('character', '')).replace(' ', '-')
        char = c.mapping(chars.get(name), f'{path}: character {name}')
        for field in ('master_profile_drive_id', 'approved_image_drive_id'):
            c.require(field in profile, f'{path}: missing {field}')
        for field, key in aliases.items():
            if field in profile:
                c.equal(profile[field], char.get(key), f'{path}.{field}')
    return c


def verify_files(check, file_map, base_dir, require_all=False):
    """Paths are relative to the map file; never download or modify source files."""
    if require_all:
        for identity in check.assets.keys() - file_map.keys():
            check.errors.append(f'{identity}: raw file missing from verification map')
    for identity, raw_path in file_map.items():
        check.attempted += 1
        if identity not in check.assets:
            check.errors.append(f'{identity}: unknown asset in file map')
            continue
        digest, label = check.assets[identity]
        if digest is None:
            check.errors.append(f'{label}: no registered hash; cannot certify bytes')
            continue
        if not isinstance(raw_path, str) or not raw_path.strip():
            check.errors.append(f'{identity}: expected a file path')
            continue
        path = Path(base_dir) / raw_path
        try:
            h = hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(block)
            if h.hexdigest() != digest:
                check.errors.append(f'{label}: SHA256 mismatch for {identity}; expected {digest}, got {h.hexdigest()}')
            else:
                check.verified += 1
        except OSError as exc:
            check.errors.append(f'{label}: cannot read raw file: {exc}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--asset-files', type=Path, help='YAML mapping of Drive IDs to raw local downloads')
    parser.add_argument('--require-all-assets', action='store_true')
    parser.add_argument('--strict', action='store_true', help='Also fail on incomplete metadata warnings')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        profiles = [(p, read_yaml(p)) for p in sorted((args.root/'CHARACTERS').glob('*/profile.yaml'))]
        check = validate(read_yaml(args.root/'CANON/source-registry.yaml'), read_yaml(args.root/'CANON/character-rules.yaml'), profiles)
        if args.asset_files:
            verify_files(check, read_yaml(args.asset_files), args.asset_files.resolve().parent, args.require_all_assets)
        elif args.require_all_assets:
            check.errors.append('--require-all-assets requires --asset-files')
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        check = Check()
        check.errors.append(str(exc))
    failed = bool(check.errors or (args.strict and check.warnings))
    result = {'status':'FAIL' if failed else 'PASS_WITH_WARNINGS' if check.warnings else 'PASS',
              'scope':'reference consistency; not visual approval or Drive availability',
              'byte_verification':'not_run' if not args.asset_files else 'failed' if check.errors else 'complete' if check.verified == len(check.assets) else 'partial',
              'registered_assets':len(check.assets), 'files_attempted':check.attempted,
              'files_verified':check.verified, 'errors':check.errors, 'warnings':check.warnings}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['status']} canon references; raw bytes: {result['byte_verification']} ({check.verified}/{len(check.assets)})")
        for key in ('errors', 'warnings'):
            for item in result[key]:
                print(f'{key.upper()}: {item}')
        print('No visual approval, source-hash repair, or FINAL LOCKED promotion is performed.')
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
