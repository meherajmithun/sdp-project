"""Validated crop catalog storage used by the crop management interface."""
import sqlite3
from contextlib import closing
from pathlib import Path

from finance_data import BASE_DIR


SOIL_TYPES = (
    'Alluvial Soil (Floodplain Soil)',
    'Red Soil (Lateritic Soil)',
    'Sandy Soil',
    'Clay Soil',
    'Loamy Soil',
    'Peaty Soil (Haor Soil)',
    'Saline Soil (Coastal Soil)',
)
LEVELS = ('Low', 'Medium', 'High')
CATEGORIES = ('Fruit', 'Vegetables', 'Crop')
SEASONS = ('Summer', 'Rainy', 'Winter', 'Monsoon')

SAMPLE_CROPS = (
    ('Rice', 120, SOIL_TYPES[0], 'High', 'High', 'Crop', 'Rainy'),
    ('Wheat', 110, 'Loamy Soil', 'High', 'Medium', 'Crop', 'Winter'),
    ('Potato', 90, 'Loamy Soil', 'High', 'Medium', 'Vegetables', 'Winter'),
    ('Tomato', 80, 'Loamy Soil', 'High', 'Medium', 'Vegetables', 'Winter'),
    ('Maize', 100, SOIL_TYPES[0], 'High', 'Medium', 'Crop', 'Summer'),
)


class CropError(ValueError):
    """A crop operation could not be completed safely."""


class DuplicateCropError(CropError):
    """A crop with the same normalized name already exists."""


class CropInUseError(CropError):
    """A crop cannot be deleted because finance records use it."""


def clean_name(value):
    """Trim a crop name and collapse repeated whitespace."""
    return ' '.join(str(value).split())


def normalized_name(value):
    return clean_name(value).casefold()


def validate_crop(crop_name, days_to_harvest, soil_type, sunlight,
                  water_req, category, season):
    name = clean_name(crop_name)
    if not name:
        raise CropError('Enter a crop name.')
    try:
        days = int(str(days_to_harvest).strip())
    except (TypeError, ValueError):
        raise CropError('Days to harvest must be a positive whole number.') from None
    if days <= 0:
        raise CropError('Days to harvest must be a positive whole number.')

    selections = (
        ('soil type', soil_type, SOIL_TYPES),
        ('sunlight requirement', sunlight, LEVELS),
        ('water requirement', water_req, LEVELS),
        ('crop category', category, CATEGORIES),
        ('season', season, SEASONS),
    )
    for label, value, allowed in selections:
        if value not in allowed:
            raise CropError(f'Select a valid {label}.')
    return name, days, soil_type, sunlight, water_req, category, season


class CropStore:
    """CRUD operations for crops, independent from Tkinter widgets."""

    def __init__(self, directory=BASE_DIR):
        self.directory = Path(directory)
        self.path = self.directory / 'crops.db'
        self.finance_path = self.directory / 'sales.db'
        self.setup()

    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def setup(self):
        with closing(self.connect()) as conn, conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS crops(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_name TEXT,
                days_to_harvest INTEGER,
                soil_type TEXT,
                sunlight TEXT,
                water_req TEXT,
                category TEXT,
                season TEXT
            )''')

    def list_crops(self):
        with closing(self.connect()) as conn:
            rows = conn.execute('''SELECT id, crop_name, days_to_harvest,
                soil_type, sunlight, water_req, category, season
                FROM crops ORDER BY crop_name COLLATE NOCASE, id''').fetchall()
        return [dict(row) for row in rows]

    def get(self, crop_id):
        with closing(self.connect()) as conn:
            row = conn.execute('''SELECT id, crop_name, days_to_harvest,
                soil_type, sunlight, water_req, category, season
                FROM crops WHERE id=?''', (crop_id,)).fetchone()
        return dict(row) if row else None

    def duplicate(self, crop_name, exclude_id=None):
        target = normalized_name(crop_name)
        for crop in self.list_crops():
            if crop['id'] != exclude_id and normalized_name(crop['crop_name']) == target:
                return crop
        return None

    def add(self, crop_name, days_to_harvest, soil_type, sunlight,
            water_req, category, season):
        values = validate_crop(crop_name, days_to_harvest, soil_type,
                               sunlight, water_req, category, season)
        duplicate = self.duplicate(values[0])
        if duplicate:
            raise DuplicateCropError(
                f"A crop named '{duplicate['crop_name']}' already exists (#{duplicate['id']}).")
        with closing(self.connect()) as conn, conn:
            cursor = conn.execute('''INSERT INTO crops
                (crop_name, days_to_harvest, soil_type, sunlight,
                 water_req, category, season)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
            return cursor.lastrowid

    def update(self, crop_id, crop_name, days_to_harvest, soil_type,
               sunlight, water_req, category, season):
        if not self.get(crop_id):
            raise CropError('The selected crop no longer exists. Refresh the list.')
        values = validate_crop(crop_name, days_to_harvest, soil_type,
                               sunlight, water_req, category, season)
        duplicate = self.duplicate(values[0], exclude_id=crop_id)
        if duplicate:
            raise DuplicateCropError(
                f"A crop named '{duplicate['crop_name']}' already exists (#{duplicate['id']}).")
        with closing(self.connect()) as conn, conn:
            conn.execute('''UPDATE crops SET crop_name=?, days_to_harvest=?,
                soil_type=?, sunlight=?, water_req=?, category=?, season=?
                WHERE id=?''', values + (crop_id,))

    @staticmethod
    def _columns(conn, table):
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone()
        return {row[1] for row in conn.execute(f'PRAGMA table_info({table})')} if exists else set()

    def reference_counts(self, crop_id):
        crop = self.get(crop_id)
        if not crop or not self.finance_path.exists():
            return {'sales': 0, 'expenses': 0}
        counts = {'sales': 0, 'expenses': 0}
        with closing(sqlite3.connect(self.finance_path)) as conn:
            sales_columns = self._columns(conn, 'sales')
            if 'crop_id' in sales_columns:
                counts['sales'] = conn.execute(
                    'SELECT COUNT(*) FROM sales WHERE crop_id=?', (crop_id,)
                ).fetchone()[0]
            elif 'crop_name' in sales_columns:
                counts['sales'] = conn.execute(
                    'SELECT COUNT(*) FROM sales WHERE lower(trim(crop_name))=lower(trim(?))',
                    (crop['crop_name'],),
                ).fetchone()[0]
            if 'crop_id' in self._columns(conn, 'expenses'):
                counts['expenses'] = conn.execute(
                    'SELECT COUNT(*) FROM expenses WHERE crop_id=?', (crop_id,)
                ).fetchone()[0]
        return counts

    def delete(self, crop_id):
        crop = self.get(crop_id)
        if not crop:
            raise CropError('The selected crop no longer exists. Refresh the list.')
        references = self.reference_counts(crop_id)
        if references['sales'] or references['expenses']:
            raise CropInUseError(
                f"'{crop['crop_name']}' is used by {references['sales']} sale(s) and "
                f"{references['expenses']} expense(s). Keep the crop to protect those records.")
        with closing(self.connect()) as conn, conn:
            conn.execute('DELETE FROM crops WHERE id=?', (crop_id,))

    def load_samples(self):
        existing = {normalized_name(crop['crop_name']) for crop in self.list_crops()}
        added = 0
        with closing(self.connect()) as conn, conn:
            for values in SAMPLE_CROPS:
                if normalized_name(values[0]) in existing:
                    continue
                conn.execute('''INSERT INTO crops
                    (crop_name, days_to_harvest, soil_type, sunlight,
                     water_req, category, season)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
                existing.add(normalized_name(values[0]))
                added += 1
        return added
