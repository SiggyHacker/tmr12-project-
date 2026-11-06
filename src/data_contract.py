"""Data contract for the Nordic Pearl / Nordic Crown AIS data (2025).

One shared definition of what "valid" data looks like.
- Cleaning (01_load_and_clean.ipynb) uses it to drop or fix rows.
- Observability (observability.ipynb) uses it to count violations, on raw and cleaned data.

Rules here must be justified WITHOUT looking at the data: the AIS standard,
ship registers, the route's geography, or our own design choices.
Write the source next to each rule. Limits not decided yet are marked TODO.

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
    "true_heading": "float",  # float, not int: AIS fields can be "not available" (missing)
    "draught": "float",       # metres
    "ais_class": "string",
}

# 2. Identity: exactly these two ships. Use MMSI as the ID.
# Source: ship registers (TODO: name the register we checked, e.g. Equasis).
SHIPS = {
    219592000: {"imo": 8917613, "names": ["NORDIC CROWN", "CROWN SEAWAYS"], "length": 171, "breadth": 28},
    219945000: {"imo": 8701674, "names": ["NORDIC PEARL", "PEARL SEAWAYS"], "length": 178, "breadth": 30},
}

# 3. Valid ranges (inclusive).
# Defined by the AIS standard (ITU-R M.1371): the allowed values of each field.
RANGES = {
    "cog": (0.0, 359.9),             # course over ground, 0.1 degree steps
    "true_heading": (0.0, 359.0),    # whole degrees
    "rot": (-127.0, 127.0),          # rate of turn, AIS-encoded value
}
# TODO: decide together, each with a source that does not come from the data:
#   "lat":     route geography (Oslo - Copenhagen), from a map
#   "lon":     route geography (Oslo - Copenhagen), from a map
#   "speed":   ship specifications (service / max speed)
#   "draught": ship specifications (design draught)

# AIS "not available" codes (ITU-R M.1371): treat as missing, not as values.
NOT_AVAILABLE = {
    "lat": [91.0],
    "lon": [181.0],
    "speed": [102.3],
    "cog": [360.0],
    "true_heading": [511.0],
    "rot": [-128.0],
}

# 4. Uniqueness and order (our design choice)
UNIQUE_KEY = ["mmsi", "date_time_utc"]   # one position per ship per timestamp
SORT_BY = ["mmsi", "date_time_utc"]

# 5. Coverage: the period we requested data for
PERIOD = ("2025-01-01", "2025-12-31")
# TODO: largest acceptable gap between messages while sailing.
#   Starting point: AIS class A ships report every 2-10 s when moving (ITU-R M.1371).
MAX_GAP_MINUTES = None

# 6. Allowed categories
ALLOWED = {
    "ais_class": ["A"],   # passenger ships must carry class A AIS (SOLAS)
}

# Columns we agree to drop, because they repeat information in another column by definition
DROP_COLUMNS = ["geom", "geometry_wkt", "callsign"]
# TODO: decide on "maneuvre" after checking its values in the observability notebook.
