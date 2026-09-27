import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from check_canon import Check, read_yaml, validate, verify_files
from check_manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[1]


class CanonTests(unittest.TestCase):
    def setUp(self):
        self.registry = read_yaml(ROOT/'CANON/source-registry.yaml')
        self.rules = read_yaml(ROOT/'CANON/character-rules.yaml')

    def check(self):
        return validate(self.registry, self.rules)

    def test_current_reference_consistency(self):
        profiles = [(p, read_yaml(p)) for p in (ROOT/'CHARACTERS').glob('*/profile.yaml')]
        self.assertEqual(validate(self.registry, self.rules, profiles).errors, [])

    def test_missing_image_hash_fails(self):
        del self.registry['characters']['Ben']['image_sha256']
        self.assertTrue(self.check().errors)

    def test_bad_hash_fails(self):
        self.registry['characters']['Ben']['image_sha256'] = 'not-a-hash'
        self.assertTrue(self.check().errors)

    def test_drive_url_is_not_an_id(self):
        self.registry['characters']['Ben']['image_id'] = 'https://drive.google.com/file/d/example'
        self.assertTrue(self.check().errors)

    def test_shared_id_conflicting_hash_fails(self):
        self.registry['characters']['Leo']['logo_sha256'] = 'a'*64
        self.assertTrue(any('conflicting hashes' in e for e in self.check().errors))

    def test_missing_profile_hash_is_explicit_debt(self):
        del self.registry['characters']['Ben']['profile_sha256']
        self.assertTrue(any('Ben.profile_sha256' in w for w in self.check().warnings))

    def test_stale_character_copy_fails(self):
        p = read_yaml(ROOT/'CHARACTERS/Ben/profile.yaml')
        p['approved_image_sha256'] = 'a'*64
        self.assertTrue(validate(self.registry, self.rules, [('Ben', p)]).errors)

    def test_wrong_emblem_link_fails(self):
        self.rules['children_vest_back_emblem']['image_id'] = 'wrong_emblem_id'
        self.assertTrue(self.check().errors)

    def test_wrong_civic_variant_fails(self):
        self.registry['characters']['Daniel-Brooks']['logo_id'] = self.registry['characters']['Elena-Rivera']['logo_id']
        self.assertTrue(self.check().errors)

    def test_unresolved_registry_key_fails(self):
        self.rules['children_vest_back_emblem']['asset_registry_key'] = 'branding_assets.missing'
        self.assertTrue(any('unresolved registry reference' in e for e in self.check().errors))

    def test_unknown_sticker_wearer_fails(self):
        self.rules['fire_station_project_sticker']['placements']['Unknown'] = 'rear'
        self.assertTrue(self.check().errors)

    def test_excluded_sticker_wearer_fails(self):
        self.rules['fire_station_project_sticker']['placements']['Rebecca-Foster'] = 'rear'
        self.assertTrue(self.check().errors)

    def test_adult_placement_conflict_fails(self):
        self.rules['fire_station_project_sticker']['placements']['Daniel-Brooks'] = 'front'
        self.assertTrue(any('sticker placement' in e for e in self.check().errors))

    def test_missing_height_record_fails(self):
        del self.rules['character_dimensions_and_helmet_colors']['characters']['Ben']
        self.assertTrue(self.check().errors)

    def test_height_order_conflict_fails(self):
        self.rules['character_dimensions_and_helmet_colors']['characters']['Ben']['standing_height_inches'] = 50
        self.assertTrue(self.check().errors)

    def test_boolean_height_fails(self):
        self.rules['character_dimensions_and_helmet_colors']['characters']['Ben']['standing_height_inches'] = True
        self.assertTrue(self.check().errors)

    def test_missing_helmet_color_fails(self):
        self.rules['character_dimensions_and_helmet_colors']['characters']['Ben']['hard_hat_color'] = None
        self.assertTrue(self.check().errors)

    def test_raw_hash_match_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'raw.bin'; path.write_bytes(b'approved bytes')
            check = Check(); digest = hashlib.sha256(path.read_bytes()).hexdigest()
            check.asset({'id':'test_drive_id_123', 'sha256':digest}, 'id', 'sha256', 'fixture')
            verify_files(check, {'test_drive_id_123':'raw.bin'}, tmp, require_all=True)
            self.assertEqual(check.verified, 1); self.assertEqual(check.errors, [])
            path.write_bytes(b'changed bytes')
            verify_files(check, {'test_drive_id_123':'raw.bin'}, tmp)
            self.assertTrue(any('SHA256 mismatch' in e for e in check.errors))

    def test_required_raw_file_missing(self):
        check = Check(); check.assets['test_drive_id_123'] = ('a'*64, 'fixture')
        verify_files(check, {}, '.', require_all=True)
        self.assertTrue(check.errors)

    def test_unknown_raw_asset_fails(self):
        check = Check(); verify_files(check, {'unknown':'raw.png'}, '.')
        self.assertTrue(check.errors)

    def test_duplicate_yaml_and_nonmapping_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'bad.yaml'
            for content in ('x: 1\nx: 2\n', '- one\n- two\n'):
                path.write_text(content)
                with self.assertRaises(ValueError):
                    read_yaml(path)

    def test_pending_spread_compatible(self):
        self.assertEqual(validate_manifest({'spread':'03-04', 'status':'DEVELOPMENT',
                         'version_b':{'status':'pending', 'path':'version-b/'}}), [])

    def test_manifest_shape_traversal_and_missing_approval(self):
        for version in (None, {'status':'pending','path':'../elsewhere'}):
            self.assertTrue(validate_manifest({'spread':'03-04','status':'DEVELOPMENT','version_b':version}))
        self.assertTrue(validate_manifest({'spread':'03-04','status':'FINAL LOCKED',
                        'version_b':{'status':'done','path':'version-b/'}, 'final_locked':True, 'approved_by':None}))


if __name__ == '__main__':
    unittest.main()
