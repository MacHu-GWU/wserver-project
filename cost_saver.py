# -*- coding: utf-8 -*-

"""
POC for cost saver lambda function data processing logic.
"""

import polars as pl
from datetime import datetime, timedelta

# this is the measurement data from DynamoDB
df = pl.DataFrame(
    {
        "time": [
            datetime(2024, 1, 1, 15, 2),
            datetime(2024, 1, 1, 15, 7),
            datetime(2024, 1, 1, 15, 9),
            datetime(2024, 1, 1, 15, 17),
            datetime(2024, 1, 1, 15, 22),
            datetime(2024, 1, 1, 15, 42),
        ],
        "value": [
            1,
            2,
            3,
            4,
            5,
            6,
        ],
    }
)

# floor to 5 minutes
floored_df = df.with_columns([pl.col("time").dt.truncate("5m")])

# only keep the first value in each 5 minutes
# for example, 15:7 and 15:9 both will floor to 15:5, we only keep 15:7 value
floored_df = floored_df.group_by("time", maintain_order=True).agg(
    [
        pl.col("value").first().alias("value"),
    ]
)
print("--- floored_df ---")
print(floored_df)

# create a reference DataFrame with all 5 minutes
# min_time = floored_df["time"].min()
# max_time = floored_df["time"].max() + timedelta(minutes=5)
min_time = datetime(2024, 1, 1, 16, 0)
max_time = datetime(2024, 1, 1, 17, 0)
reference_df = pl.DataFrame().select(
    pl.datetime_range(min_time, max_time, interval=timedelta(minutes=5)).alias("time")
)
print("--- reference_df ---")
print(reference_df)

result_df = reference_df.join(floored_df, on="time", how="left")
print("--- result_df ---")
print(result_df)

# Forward fill values within a 5-minute window
final_result_df = result_df.sort('time').select([
    'time',
    pl.col('value').forward_fill(limit=1)
])
print("--- final_result_df ---")
print(final_result_df)
