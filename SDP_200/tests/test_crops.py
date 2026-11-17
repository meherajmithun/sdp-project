import tempfile
import unittest

from crop_data import CropError, CropInUseError, CropStore, DuplicateCropError
from finance_data import FinanceStore


VALID = dict(
    crop_name='Rice',
    days_to_harvest='120',
    soil_type='Alluvial Soil (Floodplain Soil)',
    sunlight='High',
    water_req='High',
    category='Crop',
    season='Rainy',
)


class CropStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = CropStore(self.temp.name)

    def add_rice(self):
        return self.store.add(**VALID)

    def test_add_and_list_crop(self):
        crop_id = self.add_rice()
        self.assertEqual(self.store.get(crop_id)['crop_name'], 'Rice')
        self.assertEqual(self.store.list_crops()[0]['days_to_harvest'], 120)

    def test_rejects_invalid_fields(self):
        for name, value in (('crop_name', ''), ('days_to_harvest', '0'),
                            ('days_to_harvest', '-1'), ('days_to_harvest', '2.5'),
                            ('soil_type', 'Unknown soil'), ('season', 'Autumn')):
            values = dict(VALID)
            values[name] = value
            with self.subTest(name=name, value=value), self.assertRaises(CropError):
                self.store.add(**values)
        self.assertEqual(self.store.list_crops(), [])

    def test_duplicate_names_ignore_case_and_whitespace(self):
        self.add_rice()
        values = dict(VALID, crop_name='  RICE  ')
        with self.assertRaises(DuplicateCropError):
            self.store.add(**values)

    def test_update_crop_and_prevent_duplicate(self):
        rice_id = self.add_rice()
        wheat = dict(VALID, crop_name='Wheat', days_to_harvest='110',
                     soil_type='Loamy Soil', water_req='Medium', season='Winter')
        wheat_id = self.store.add(**wheat)
        updated = dict(VALID, crop_name='Aman Rice', days_to_harvest='135')
        self.store.update(rice_id, **updated)
        self.assertEqual(self.store.get(rice_id)['crop_name'], 'Aman Rice')
        with self.assertRaises(DuplicateCropError):
            self.store.update(wheat_id, **dict(wheat, crop_name=' aman   rice '))

    def test_delete_unused_crop(self):
        crop_id = self.add_rice()
        self.store.delete(crop_id)
        self.assertIsNone(self.store.get(crop_id))

    def test_delete_referenced_crop_is_blocked(self):
        crop_id = self.add_rice()
        finance = FinanceStore(self.temp.name)
        finance.add_sale(crop_id, '10', '25', '17-11-2026')
        finance.add_expense(crop_id, 'Seeds', '100', '17-11-2026')
        with self.assertRaises(CropInUseError) as error:
            self.store.delete(crop_id)
        self.assertIn('1 sale(s)', str(error.exception))
        self.assertIsNotNone(self.store.get(crop_id))

    def test_sample_loading_is_repeat_safe(self):
        first = self.store.load_samples()
        second = self.store.load_samples()
        self.assertEqual(first, 5)
        self.assertEqual(second, 0)
        self.assertEqual(len(self.store.list_crops()), 5)


if __name__ == '__main__':
    unittest.main()
