# Analysis of the occupancy dip between $3.25 and $4.25 price midpoints
# Goal: isolate the dip spaces, see which areas and streets they sit on,
# and compare them to the rest of the data.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# --- Load data ---------------------------------------------------------------
# TODO: point this at the same file(s) you built df from in your main notebook
DATA_PATH = Path("your_data_file.csv")
df = pd.read_csv(DATA_PATH)


# --- Define the dip ----------------------------------------------------------
# dip range taken from the binned plot: occupancy drops from $3.25 to $4.25
DIP_LOW, DIP_HIGH = 3.25, 4.25

dip_df = df[df['price_midpoint'].between(DIP_LOW, DIP_HIGH)].copy()
rest_df = df[~df['price_midpoint'].between(DIP_LOW, DIP_HIGH)].copy()

print(f"Dip spaces: {len(dip_df)} | Rest: {len(rest_df)}")


# --- Area prefix (CB, CC, HO, LT, ...) ---------------------------------------
dip_df['area'] = dip_df['SpaceID'].str.extract(r'^([A-Z]+)')
rest_df['area'] = rest_df['SpaceID'].str.extract(r'^([A-Z]+)')


# --- Street names from BlockFace ("800 HOPE ST" -> "HOPE ST") ----------------
dip_df['street'] = dip_df['BlockFace'].str.replace(r'^\d+\s+', '', regex=True)


# --- Street summary for the dip ----------------------------------------------
street_summary = (
    dip_df.groupby('street')
    .agg(n_spaces=('SpaceID', 'count'),
         n_blocks=('BlockFace', 'nunique'),
         mean_occ=('occupancy_rate', 'mean'),
         prices=('price_midpoint', lambda s: sorted(s.unique())))
    .sort_values('n_spaces', ascending=False)
)

print("\nStreets in the dip:")
print(street_summary)