"""Spotless ECON 430: analysis source exported from the report notebooks."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[1] / 'notebooks/cleaning')

# 01_clean_occupancy
# 01 — Clean Occupancy Data
# 1. Load the raw transactions
import pandas as pd

occupancy = pd.read_csv("../../data/raw/ladot_occupancy/20261017T052111914317Z/Sensor Transactions_2025_08.csv")

occupancy.head()

# 2. Check the records and timestamps
print("Rows and columns:", occupancy.shape)

print("\nColumn types:")
print(occupancy.dtypes)

print("\nUnique parking spaces:")
print(occupancy["SpaceID"].nunique())

occupancy.isnull().sum()


print("Occupancy states:")
print(occupancy["OccupancyState"].value_counts())


print("\nExact duplicate rows:")
print(occupancy.duplicated().sum())


occupancy["EventTime_Local"] = pd.to_datetime(occupancy["EventTime_Local"], format="%m/%d/%Y %I:%M:%S %p")

print("\nTime range:")
print(occupancy["EventTime_Local"].min())
print(occupancy["EventTime_Local"].max())

# 3. Inspect coverage across parking spaces
space_counts = occupancy.groupby("SpaceID").size()

space_counts.describe()

coverage = occupancy.groupby("SpaceID")["EventTime_Local"].agg(["min", "max", "count"])

coverage["days_covered"] = (coverage["max"] - coverage["min"]).dt.days

coverage["days_covered"].describe()

occupancy["date"] = occupancy["EventTime_Local"].dt.date

active_days = occupancy.groupby("SpaceID")["date"].nunique()

active_days.describe()

# 4. Inspect one space’s event sequence
example = occupancy[occupancy["SpaceID"] == "WV308"]

example.head(15)

# 5. Measure time in each recorded state
occupancy = occupancy.sort_values(["SpaceID", "EventTime_Local"])

occupancy["next_time"] = occupancy.groupby("SpaceID")["EventTime_Local"].shift(-1)

occupancy["duration_minutes"] = (
    occupancy["next_time"] - occupancy["EventTime_Local"]
).dt.total_seconds() / 60

occupancy[["SpaceID", "EventTime_Local", "OccupancyState", "next_time", "duration_minutes"]].head(15)

# 6. Inspect long gaps between events
occupancy["duration_minutes"].describe(percentiles=[0.5, 0.9, 0.95, 0.99])

print("Over 12 hours:", (occupancy["duration_minutes"] > 720).sum())
print("Over 24 hours:", (occupancy["duration_minutes"] > 1440).sum())
print("Over 48 hours:", (occupancy["duration_minutes"] > 2880).sum())
print("Over 72 hours:", (occupancy["duration_minutes"] > 4320).sum())

# 7. Identify valid intervals
occupancy["valid_duration"] = (
    occupancy["duration_minutes"].notna()
    & (occupancy["duration_minutes"] <= 1440)
    & (occupancy["OccupancyState"] != "UNKNOWN")
)

occupancy["valid_duration"].value_counts()

# 8. Calculate the monthly occupancy rate
valid = occupancy[occupancy["valid_duration"]].copy()

valid["occupied_minutes"] = valid["duration_minutes"].where(
    valid["OccupancyState"] == "OCCUPIED", 0
)

space_occupancy = valid.groupby("SpaceID").agg(
    occupied_minutes=("occupied_minutes", "sum"),
    total_minutes=("duration_minutes", "sum")
)

space_occupancy["occupancy_rate"] = (
    space_occupancy["occupied_minutes"] / space_occupancy["total_minutes"]
)

space_occupancy["occupancy_rate"].describe()

# 9. Require at least 25 active calendar days
space_occupancy["active_days"] = active_days

space_occupancy = space_occupancy[
    space_occupancy["active_days"] >= 25
].copy()

print("Final number of spaces:", len(space_occupancy))

space_occupancy["occupancy_rate"].describe()

# 10. Save the parking-space cross-section
space_occupancy = space_occupancy.reset_index()

space_occupancy.to_csv(
    "../../data/processed/space_occupancy_aug2025.csv",
    index=False
)

space_occupancy.head()

# Summary
# 02_clean_meter_inventory
# 02 — Clean Meter Inventory
# 1. Load the raw meter inventory
import pandas as pd

meters = pd.read_csv(
    "../../data/raw/ladot_meters/20261017T052111914317Z/inventory.csv"
)

meters.head()

# 2. Check the inventory structure and categories
print("Rows and columns:", meters.shape)

print("\nColumn types:")
print(meters.dtypes)

print("\nMissing values:")
print(meters.isnull().sum())

print("\nUnique SpaceIDs:", meters["SpaceID"].nunique())
print("Duplicate SpaceIDs:", meters["SpaceID"].duplicated().sum())

print("Meter types:")
print(meters["MeterType"].value_counts())

print("\nRate types:")
print(meters["RateType"].value_counts())

print("\nRate ranges:")
print(meters["RateRange"].value_counts().head(15))

print("\nTime limits:")
print(meters["MeteredTimeLimit"].value_counts())

# 3. Confirm and remove exact duplicate records
duplicate_ids = meters[meters["SpaceID"].duplicated(keep=False)]

duplicate_ids.sort_values("SpaceID")

meters = meters.drop_duplicates().copy()

print("Rows after removing duplicates:", len(meters))
print("Unique SpaceIDs:", meters["SpaceID"].nunique())
print("Duplicate SpaceIDs:", meters["SpaceID"].duplicated().sum())

# 4. Express parking time limits in hours
meters["MeteredTimeLimit"].value_counts().sort_index()

time_map = {
    "15MIN": 0.25,
    "30MIN": 0.5,
    "1HR": 1,
    "2HR": 2,
    "2HR-30MIN": 2.5,
    "4HR": 4,
    "6HR": 6,
    "7HR": 7,
    "10HR": 10,
    "13HR": 13,
    "14HR": 14
}

meters["time_limit_hours"] = meters["MeteredTimeLimit"].map(time_map)

meters["time_limit_hours"].describe()

# 5. Inspect pricing structures and extract dollar amounts
for rate_type in ["FLAT", "TOD", "JUMP"]:
    print("\n", rate_type)
    print(
        meters[meters["RateType"] == rate_type]["RateRange"]
        .value_counts()
        .head(15)
    )

meters["price_numbers"] = meters["RateRange"].str.findall(r"\$(\d+(?:\.\d+)?)")

meters[["RateType", "RateRange", "price_numbers"]].head(15)

# 6. Construct the price proxy and numeric coordinates
meters["price_numbers"] = meters["RateRange"].str.findall(r"\$(\d+(?:\.\d+)?)")

meters["price_numbers"] = meters["price_numbers"].apply(
    lambda x: [float(i) for i in x]
)

meters["price_midpoint"] = meters["price_numbers"].apply(
    lambda x: sum(x) / len(x) if len(x) > 0 else None
)

meters[["latitude", "longitude"]] = (
    meters["LatLng"]
    .str.strip("()")
    .str.split(",", expand=True)
    .astype(float)
)

print(meters[["RateType", "RateRange", "price_midpoint"]].head(10))

print("\nPrice summary:")
print(meters["price_midpoint"].describe())

print("\nCoordinate summary:")
print(meters[["latitude", "longitude"]].describe())

# 7. Validate the numeric variables
print("Missing time limits:", meters["time_limit_hours"].isnull().sum())
print("Missing prices:", meters["price_midpoint"].isnull().sum())
print("Missing latitude:", meters["latitude"].isnull().sum())
print("Missing longitude:", meters["longitude"].isnull().sum())

print("\nTime limit summary:")
print(meters["time_limit_hours"].describe())

# 8. Check matches to the cleaned occupancy sample
occupancy_clean = pd.read_csv(
    "../../data/processed/space_occupancy_aug2025.csv"
)

matched = occupancy_clean.merge(
    meters,
    on="SpaceID",
    how="left",
    indicator=True
)

print(matched["_merge"].value_counts())

print("\nMatched percentage:")
print((matched["_merge"] == "both").mean() * 100)

unmatched = matched[matched["_merge"] != "both"]

print("Unmatched spaces:", len(unmatched))

unmatched[["SpaceID", "occupancy_rate", "active_days"]].head(20)

# 9. Save the cleaned meter inventory
meters_clean = meters[
    [
        "SpaceID",
        "BlockFace",
        "MeterType",
        "RateType",
        "RateRange",
        "MeteredTimeLimit",
        "price_midpoint",
        "time_limit_hours",
        "latitude",
        "longitude"
    ]
].copy()

meters_clean.to_csv(
    "../../data/processed/meter_inventory_clean.csv",
    index=False
)

meters_clean.head()

# Summary
# 03_build_cross_section
# 03 — Build Cross-Section
# 1. Load the prepared parking data
import json
from pathlib import Path
from collections import Counter

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely import build_area
from shapely.geometry import MultiLineString

occupancy = pd.read_csv("../../data/processed/space_occupancy_aug2025.csv", dtype={"SpaceID": str})
meters = pd.read_csv("../../data/processed/meter_inventory_clean.csv", dtype={"SpaceID": str})

print("Occupancy rows:", len(occupancy))
print("Inventory rows:", len(meters))
print("Occupancy duplicate IDs:", occupancy["SpaceID"].duplicated().sum())
print("Inventory duplicate IDs:", meters["SpaceID"].duplicated().sum())
occupancy.head()

# 2. Match occupancy to meter characteristics
parking_match = occupancy.merge(meters, on="SpaceID", how="left", indicator=True, validate="one_to_one")
print(parking_match["_merge"].value_counts())
print("Match percentage:", (parking_match["_merge"] == "both").mean() * 100)

unmatched_meters = parking_match.loc[parking_match["_merge"] == "left_only"]
print("Unmatched spaces:", len(unmatched_meters))
unmatched_meters[["SpaceID", "occupancy_rate", "active_days"]].head(20)

parking = parking_match.loc[parking_match["_merge"] == "both"].drop(columns="_merge").copy()
print("Base shape:", parking.shape)
print("Unique SpaceIDs:", parking["SpaceID"].nunique())
print("Duplicate SpaceIDs:", parking["SpaceID"].duplicated().sum())
parking[["SpaceID", "occupancy_rate", "price_midpoint", "latitude", "longitude"]].head()

# 3. Read the Census estimates by tract
acs_path = Path("../../data/raw/census/20261017T052111914317Z/acs2024_5yr_la_county_tracts.json")
with acs_path.open() as f:
    acs_raw = json.load(f)

print("ACS release:", acs_raw["release"])
acs_rows = []
for geography, tables in acs_raw["data"].items():
    acs_rows.append({
        "GEOID": geography.replace("14000US", ""),
        "population": tables["B01003"]["estimate"]["B01003001"],
        "median_income": tables["B19013"]["estimate"]["B19013001"],
        "housing_units": tables["B25001"]["estimate"]["B25001001"],
        "commuters": tables["B08301"]["estimate"]["B08301001"],
        "drive_alone": tables["B08301"]["estimate"]["B08301003"],
        "public_transit": tables["B08301"]["estimate"]["B08301010"],
        "walked": tables["B08301"]["estimate"]["B08301019"]
    })
acs = pd.DataFrame(acs_rows)
print("ACS shape:", acs.shape)
print("Duplicate tract IDs:", acs["GEOID"].duplicated().sum())
print("Missing estimates:")
print(acs.isna().sum())
acs.head()

# 4. Construct commuting shares and densities
acs["drive_alone_share"] = acs["drive_alone"] / acs["commuters"].where(acs["commuters"] > 0)
acs["transit_share"] = acs["public_transit"] / acs["commuters"].where(acs["commuters"] > 0)
acs["walk_share"] = acs["walked"] / acs["commuters"].where(acs["commuters"] > 0)
print(acs[["drive_alone_share", "transit_share", "walk_share"]].describe())

gazetteer = pd.read_csv(
    "../../data/raw/census/20261017T052111914317Z/2024_gaz_tracts_06.txt",
    sep="\t", dtype={"GEOID": str}
)
gazetteer.columns = gazetteer.columns.str.strip()
acs = acs.merge(gazetteer[["GEOID", "ALAND_SQMI"]], on="GEOID", how="left", indicator=True, validate="one_to_one")
print("Gazetteer matches:")
print(acs["_merge"].value_counts())
acs = acs.drop(columns="_merge")
print("Tracts with zero/nonpositive land area:", (acs["ALAND_SQMI"] <= 0).sum())
print("Tracts with missing land area:", acs["ALAND_SQMI"].isna().sum())

acs["population_density"] = acs["population"] / acs["ALAND_SQMI"].where(acs["ALAND_SQMI"] > 0)
acs["housing_density"] = acs["housing_units"] / acs["ALAND_SQMI"].where(acs["ALAND_SQMI"] > 0)
print("Nonmissing tract densities:")
print(acs[["population_density", "housing_density"]].count())
acs[["ALAND_SQMI", "population_density", "housing_density"]].describe()

# 5. Load the official tract polygons
tracts_ca = gpd.read_file("../../data/raw/census/tigerline_2024_california_tracts/tl_2024_06_tract.shp")
tracts_la = tracts_ca.loc[(tracts_ca["STATEFP"] == "06") & (tracts_ca["COUNTYFP"] == "037")].copy()
print("California tracts:", len(tracts_ca))
print("Los Angeles County tracts:", len(tracts_la))
print("Source CRS:", tracts_la.crs)
print("Duplicate GEOIDs:", tracts_la["GEOID"].duplicated().sum())
print("Invalid tract geometries:", (~tracts_la.geometry.is_valid).sum())
tracts_la[["STATEFP", "COUNTYFP", "TRACTCE", "GEOID"]].head()

# 6. Assign parking spaces to Census tracts
plausible_coordinates = parking["latitude"].between(32, 35.5) & parking["longitude"].between(-120, -116)
print("Matched spaces with missing coordinates:", parking[["latitude", "longitude"]].isna().any(axis=1).sum())
print("Matched spaces outside broad Southern California bounds:", (~plausible_coordinates).sum())
print(parking.loc[~plausible_coordinates, ["SpaceID", "latitude", "longitude"]].head())
assert plausible_coordinates.all(), "Review implausible parking coordinates before geographic matching."

parking_points = gpd.GeoDataFrame(
    parking.copy(), geometry=gpd.points_from_xy(parking["longitude"], parking["latitude"]), crs="EPSG:4326"
)
tract_match = gpd.sjoin(parking_points, tracts_la[["GEOID", "geometry"]].to_crs(parking_points.crs), how="left", predicate="within")
print("Starting parking spaces:", len(parking_points))
print("Assigned tract:", tract_match["GEOID"].notna().sum())
print("Unmatched:", tract_match["GEOID"].isna().sum())
print("Match percentage:", tract_match["GEOID"].notna().mean() * 100)
print("Unique SpaceIDs:", tract_match["SpaceID"].nunique())
print("Duplicated SpaceIDs after join:", tract_match["SpaceID"].duplicated().sum())
print(tract_match.loc[tract_match["GEOID"].isna(), ["SpaceID", "latitude", "longitude"]].head(20))
assert not tract_match["SpaceID"].duplicated().any(), "Inspect multiple tract matches before continuing."
parking_geo = tract_match.drop(columns="index_right").copy()
parking_geo["tract_match_status"] = np.where(parking_geo["GEOID"].notna(), "matched", "unmatched")

# 7. Attach the ACS candidate predictors
parking_geo = parking_geo.merge(acs, on="GEOID", how="left", indicator=True, validate="many_to_one")
print("ACS merge status:")
print(parking_geo["_merge"].value_counts())
parking_geo["acs_match_status"] = np.where(parking_geo["_merge"] == "both", "matched", "unmatched")
parking_geo = parking_geo.drop(columns="_merge")
census_variables = ["population", "median_income", "housing_units", "population_density", "housing_density", "drive_alone_share", "transit_share", "walk_share"]
print("Missing Census predictors:")
print(parking_geo[census_variables].isna().sum())
print(parking_geo[census_variables].describe())
parking_geo[["SpaceID", "occupancy_rate", "price_midpoint", "GEOID"] + census_variables].head()

# 8. Inspect the business registry
businesses = pd.read_csv(
    "../../data/raw/points_of_interest/20261017T052111914317Z/active_businesses.csv",
    dtype={"LOCATION ACCOUNT #": str, "NAICS": str}, low_memory=False
)
print("Raw business records:", len(businesses))
print("Columns:", businesses.columns.tolist())
print("Missing LOCATION:", businesses["LOCATION"].isna().sum())
print("Exact duplicate rows:", businesses.duplicated().sum())
print("Duplicate location account IDs:", businesses["LOCATION ACCOUNT #"].duplicated().sum())
print("Missing NAICS:", businesses["NAICS"].isna().sum())
print(businesses["PRIMARY NAICS DESCRIPTION"].value_counts().head(10))
businesses[["LOCATION ACCOUNT #", "NAICS", "PRIMARY NAICS DESCRIPTION", "LOCATION"]].head()

# 9. Prepare located businesses and a transparent activity subset
businesses = businesses.drop_duplicates().copy()
business_coordinates = businesses["LOCATION"].str.extract(r"\(\s*([-0-9.]+)\s*,\s*([-0-9.]+)\s*\)")
businesses["business_latitude"] = pd.to_numeric(business_coordinates[0], errors="coerce")
businesses["business_longitude"] = pd.to_numeric(business_coordinates[1], errors="coerce")
usable_locations = (
    businesses["business_latitude"].between(-90, 90)
    & businesses["business_longitude"].between(-180, 180)
    & ~((businesses["business_latitude"] == 0) & (businesses["business_longitude"] == 0))
)
print("Distinct business records:", len(businesses))
print("Records with usable locations:", usable_locations.sum())
print("Excluded from spatial counting for location issues:", (~usable_locations).sum())
businesses_located = businesses.loc[usable_locations].copy()
businesses_located["restaurant_retail"] = businesses_located["NAICS"].fillna("").str.startswith(("722", "44", "45"))
print("Located food-service/retail records:", businesses_located["restaurant_retail"].sum())
business_points = gpd.GeoDataFrame(
    businesses_located[["LOCATION ACCOUNT #", "restaurant_retail"]].copy(),
    geometry=gpd.points_from_xy(businesses_located["business_longitude"], businesses_located["business_latitude"]), crs="EPSG:4326"
)

# 10. Count businesses within a quarter mile
radius_miles = 0.25
radius_metres = radius_miles * 1609.344
parking_projected = parking_geo.to_crs("EPSG:26911")
business_projected = business_points.to_crs(parking_projected.crs)
finite_business_points = np.isfinite(business_projected.geometry.x) & np.isfinite(business_projected.geometry.y)
print("Nonfinite projected business locations:", (~finite_business_points).sum())
business_projected = business_projected.loc[finite_business_points].copy()
parking_buffers = parking_projected[["SpaceID", "geometry"]].copy()
parking_buffers["geometry"] = parking_buffers.geometry.buffer(radius_metres)
business_matches = gpd.sjoin(parking_buffers, business_projected, how="left", predicate="intersects")
business_counts = business_matches.groupby("SpaceID").agg(
    nearby_business_count=("index_right", "count"),
    nearby_restaurant_retail_count=("restaurant_retail", "sum")
)
parking_geo = parking_geo.merge(business_counts, on="SpaceID", how="left", validate="one_to_one")
parking_geo[["nearby_business_count", "nearby_restaurant_retail_count"]] = parking_geo[["nearby_business_count", "nearby_restaurant_retail_count"]].astype("int64")
print("Radius in miles / metres:", radius_miles, radius_metres)
print("Parking spaces receiving counts:", parking_geo["nearby_business_count"].notna().sum())
print(parking_geo[["nearby_business_count", "nearby_restaurant_retail_count"]].describe())
parking_geo[["SpaceID", "nearby_business_count", "nearby_restaurant_retail_count"]].head(10)

# 11. Read and validate the zoning batches
original_zoning_files = sorted(Path("../../data/raw/land_use").glob("20261017*/zoning_offset_*.json"))
supplement_folder = Path("../../data/raw/land_use/supplement_20261022")
supplement_names = ["zoning_offset_035000.json", "zoning_offset_055000.json"]
zoning_files = [supplement_folder / path.name if path.name in supplement_names else path for path in original_zoning_files]
zoning_attributes = []
zoning_geometry = []
zoning_reference = []
for path in zoning_files:
    with path.open() as f:
        batch = json.load(f)
    zoning_reference.append(batch["spatialReference"])
    for feature in batch["features"]:
        zoning_attributes.append(feature["attributes"])
        zoning_geometry.append(build_area(MultiLineString(feature["geometry"]["rings"])))
zoning = gpd.GeoDataFrame(zoning_attributes, geometry=zoning_geometry, crs="EPSG:3857")
print("Zoning pages:", len(zoning_files))
print("Raw feature count:", len(zoning))
with Path("../../data/raw/land_use/20261017T052654015392Z/zoning_source_ids.json").open() as f:
    original_zoning_ids = json.load(f)["objectIds"]
print("New source IDs outside the original listing:", (~zoning["OBJECTID"].isin(original_zoning_ids)).sum())
zoning = zoning.loc[zoning["OBJECTID"].isin(original_zoning_ids)].copy()
print("Features within the original ID coverage:", len(zoning))
original_id_counts = Counter(original_zoning_ids)
working_id_counts = Counter(zoning["OBJECTID"])
print("Source IDs with changed multiplicities:", sum(working_id_counts[k] != original_id_counts[k] for k in original_id_counts))
print("All original distinct IDs represented:", set(working_id_counts) == set(original_id_counts))
assert set(working_id_counts) == set(original_id_counts)
print("Source spatial references:", {str(v) for v in zoning_reference})
print("Fields:", zoning.columns.tolist())
print("Geometry types:")
print(zoning.geom_type.value_counts())
print("Repeated source IDs:", zoning["OBJECTID"].duplicated().sum())
print("Exact duplicate features:", zoning.duplicated().sum())
print("Empty geometries:", zoning.geometry.is_empty.sum())
print("Invalid geometries:", (~zoning.geometry.is_valid).sum())
zoning.loc[zoning["OBJECTID"].duplicated(keep=False), ["OBJECTID", "ZONE_CMPLT", "ZONE_CLASS", "ZONING_DESCRIPTION"]].head(12)

# 12. Match the available zoning polygons
zoning = zoning.drop_duplicates().copy()
print("Features after exact duplicate removal:", len(zoning))
print("Remaining repeated source IDs:", zoning["OBJECTID"].duplicated().sum())
print("Source descriptions:")
print(zoning["ZONING_DESCRIPTION"].value_counts().head(15))
assert zoning.geometry.is_valid.all(), "Inspect invalid zoning geometry before spatial matching."
print("Source records with empty polygon areas:")
print(zoning.loc[zoning.geometry.is_empty, ["OBJECTID", "ZONE_CMPLT", "ZONE_CLASS"]].head(15))
zoning = zoning.loc[~zoning.geometry.is_empty].copy()
print("Nonempty features used for matching:", len(zoning))
zoning_match = gpd.sjoin(
    parking_geo[["SpaceID", "geometry"]].to_crs(zoning.crs),
    zoning[["ZONE_CMPLT", "ZONE_CLASS", "ZONING_DESCRIPTION", "geometry"]],
    how="left", predicate="within"
)
print("Rows after zoning join:", len(zoning_match))
print("Extra repeated SpaceIDs:", zoning_match["SpaceID"].duplicated().sum())
print("Spaces with multiple polygon matches:", zoning_match.loc[zoning_match["SpaceID"].duplicated(keep=False), "SpaceID"].nunique())
zoning_match.loc[zoning_match["SpaceID"].duplicated(keep=False), ["SpaceID", "ZONE_CMPLT", "ZONE_CLASS", "ZONING_DESCRIPTION"]].head(20)

zoning_labels = zoning_match[["SpaceID", "ZONE_CMPLT", "ZONE_CLASS", "ZONING_DESCRIPTION"]].drop_duplicates()
ambiguous_zoning_ids = zoning_labels.loc[zoning_labels["SpaceID"].duplicated(keep=False), "SpaceID"].unique()
print("Spaces with conflicting zoning labels:", len(ambiguous_zoning_ids))
print(zoning_labels.loc[zoning_labels["SpaceID"].isin(ambiguous_zoning_ids)].head(20))
zoning_labels = zoning_labels.loc[~zoning_labels["SpaceID"].isin(ambiguous_zoning_ids)].copy()
zoning_labels = zoning_labels.rename(columns={"ZONE_CMPLT": "zoning_code", "ZONE_CLASS": "zoning_class", "ZONING_DESCRIPTION": "zoning_description"})
zoning_labels[["zoning_code", "zoning_class", "zoning_description"]] = zoning_labels[["zoning_code", "zoning_class", "zoning_description"]].replace(r"^\s*$", pd.NA, regex=True)
parking_geo = parking_geo.merge(zoning_labels, on="SpaceID", how="left", validate="one_to_one")
parking_geo["zoning_match_status"] = np.where(parking_geo["zoning_code"].notna(), "matched", "unmatched")
parking_geo.loc[parking_geo["SpaceID"].isin(ambiguous_zoning_ids), "zoning_match_status"] = "ambiguous"
print("Zoning match status:")
print(parking_geo["zoning_match_status"].value_counts())
print("Assigned zoning percentage:", (parking_geo["zoning_match_status"] == "matched").mean() * 100)
print("Duplicate parking IDs:", parking_geo["SpaceID"].duplicated().sum())
print(parking_geo["zoning_code"].value_counts().head(10))
print(parking_geo["zoning_description"].value_counts().head(10))
parking_geo.loc[parking_geo["zoning_match_status"] != "matched", ["SpaceID", "latitude", "longitude", "zoning_match_status"]].head(15)

# 13. Assemble one row per parking space
final_columns = [
    "SpaceID", "occupancy_rate", "occupied_minutes", "total_minutes", "active_days",
    "BlockFace", "MeterType", "RateType", "RateRange", "MeteredTimeLimit",
    "price_midpoint", "time_limit_hours", "latitude", "longitude", "GEOID",
    "population", "median_income", "housing_units", "commuters", "drive_alone", "public_transit", "walked",
    "ALAND_SQMI", "population_density", "housing_density", "drive_alone_share", "transit_share", "walk_share",
    "nearby_business_count", "nearby_restaurant_retail_count", "zoning_code", "zoning_class", "zoning_description",
    "tract_match_status", "acs_match_status", "zoning_match_status"
]
parking_cross_section = pd.DataFrame(parking_geo[final_columns]).copy()
print("Final rows and columns:", parking_cross_section.shape)
print("Unique SpaceIDs:", parking_cross_section["SpaceID"].nunique())
print("Duplicate SpaceIDs:", parking_cross_section["SpaceID"].duplicated().sum())
assert len(parking_cross_section) == len(parking)
assert not parking_cross_section["SpaceID"].duplicated().any()
parking_cross_section.head()

# 14. Validate the candidate variables
candidate_variables = [
    "price_midpoint", "time_limit_hours", "MeterType", "RateType", "latitude", "longitude",
    "population", "median_income", "housing_units", "population_density", "housing_density",
    "drive_alone_share", "transit_share", "walk_share", "nearby_business_count",
    "nearby_restaurant_retail_count", "zoning_code", "zoning_class", "zoning_description"
]
missingness = pd.DataFrame({
    "missing_count": parking_cross_section[candidate_variables].isna().sum(),
    "missing_percent": parking_cross_section[candidate_variables].isna().mean() * 100
})
print(missingness)
numeric_candidates = parking_cross_section[candidate_variables].select_dtypes(include="number").columns.tolist()
print(parking_cross_section[["occupancy_rate"] + numeric_candidates].describe().T)
for variable in ["MeterType", "RateType", "zoning_class", "zoning_description"]:
    print("\n", variable)
    print(parking_cross_section[variable].value_counts(dropna=False).head(12))

print("Occupancy outside [0, 1]:", (~parking_cross_section["occupancy_rate"].between(0, 1)).sum())
print("Latitude range:", parking_cross_section["latitude"].min(), parking_cross_section["latitude"].max())
print("Longitude range:", parking_cross_section["longitude"].min(), parking_cross_section["longitude"].max())
for variable in ["drive_alone_share", "transit_share", "walk_share"]:
    values = parking_cross_section[variable].dropna()
    print(variable, "range:", values.min(), values.max(), "outside [0, 1]:", (~values.between(0, 1)).sum())
nonnegative_variables = [
    "occupied_minutes", "total_minutes", "active_days", "price_midpoint", "time_limit_hours",
    "population", "median_income", "housing_units", "commuters", "drive_alone", "public_transit", "walked",
    "ALAND_SQMI", "population_density", "housing_density", "nearby_business_count", "nearby_restaurant_retail_count"
]
print("Negative values in nonnegative quantities:")
print((parking_cross_section[nonnegative_variables] < 0).sum())
print("Nonfinite nonmissing numeric values:", np.isinf(parking_cross_section.select_dtypes(include="number")).sum().sum())
print("Business subset count above all-business count:", (parking_cross_section["nearby_restaurant_retail_count"] > parking_cross_section["nearby_business_count"]).sum())
assert parking_cross_section["occupancy_rate"].between(0, 1).all()
assert parking_cross_section["active_days"].ge(25).all()

# 15. Save the cross-section for later analysis
output_path = Path("../../data/processed/parking_cross_section.csv")
parking_cross_section.to_csv(output_path, index=False)
print("Saved shape:", parking_cross_section.shape)
print("Saved path:", output_path)
parking_cross_section[["SpaceID", "occupancy_rate", "price_midpoint", "GEOID", "population_density", "nearby_business_count", "zoning_class"]].head()

# Summary
