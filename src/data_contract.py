"""Data contract for the Nordic Pearl / Nordic Crown AIS data (2025).

One shared definition of what "valid" data looks like.
- Cleaning (01_load_and_clean.ipynb) uses it to drop or fix rows.
- Observability (observability.ipynb) uses it to count violations, on raw and cleaned data.

If you change a rule, change it here so both notebooks stay in sync.
"""

# 1. Schema: columns we rely on, and their expected kind of type.
# Kinds, not exact pandas types: the exact names change between pandas versions
# (e.g. datetime64[ns] vs datetime64[us], object vs str) without the data changing.
REQUIRED_COLUMNS = {
    "date_time_utc": "datetime",
    "mmsi": "int",
    "imo": "int",
    "ship_name": "string",
    "lon": "float",
    "lat": "float",
    "speed": "float",         # SOG, knots
    "cog": "float",           # degrees
    "true_heading": "float",  # float, not int: it has missing values
    "draught": "float",       # metres
    "ais_class": "string",
}

# 2. Identity: exactly these two ships. Use MMSI as the ID (both ships were renamed in 2025).
SHIPS = {
    219592000: {"imo": 8917613, "names": ["NORDIC CROWN", "CROWN SEAWAYS"], "length": 171, "breadth": 28},
    219945000: {"imo": 8701674, "names": ["NORDIC PEARL", "PEARL SEAWAYS"], "length": 178, "breadth": 30},
}

# 3. Valid ranges (inclusive). Values outside are errors or AIS "not available" codes.
RANGES = {
    "lat": (55.0, 60.0),          # Oslo-Copenhagen area
    "lon": (8.5, 13.5),
    "speed": (0.0, 25.0),         # service speed ~16-18 kn, max well below 25
    "cog": (0.0, 359.9),
    "true_heading": (0.0, 359.0),
    "draught": (5.5, 7.5),        # observed 6.1-6.5 m; 11.8 m is an error
    "rot": (-127.0, 127.0),
}

# AIS "not available" codes (ITU-R M.1371), treat as missing, not as values
NOT_AVAILABLE = {
    "lat": [91.0],
    "lon": [181.0],
    "cog": [360.0, 511.0],
    "true_heading": [511.0],
    "rot": [-128.0],
}

# 4. Uniqueness and order
UNIQUE_KEY = ["mmsi", "date_time_utc"]   # one position per ship per timestamp
SORT_BY = ["mmsi", "date_time_utc"]

# 5. Coverage: period, and the largest acceptable gap between messages while sailing
PERIOD = ("2025-01-01", "2025-12-31")
MAX_GAP_MINUTES = 10

# 6. Allowed categories
ALLOWED = {
    "ais_class": ["A", "LRIT"],   # LRIT = low-rate satellite positions, keep separate
}

# Columns we agree to drop (no information)
DROP_COLUMNS = ["maneuvre", "geom", "geometry_wkt", "callsign"]
