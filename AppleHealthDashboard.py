import datetime
import math
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from shiny.express import render, ui

# Get the app directory
app_dir = os.path.dirname(__file__)

# Data directory
data_dir = 'data'
data_dir = os.path.join(app_dir, data_dir)

# Data file
file = 'AppleHealth_BodyMass.csv'
file = os.path.join(data_dir, file)
if not os.path.exists(file):
    raise ValueError("File not found: {}".format(file))

# Import data
df_weight = pd.read_csv(file)

# Drop the first entry and select desired columns
df_weight = df_weight.loc[1:,['sourceName','unit','startDate', 'value']]

# Rename columns
df_weight = df_weight.rename(columns = {'sourceName':'Source', 
                                        'unit':'Unit',
                                        'startDate':'Date', 
                                        'value':'Weight'})

# Convert date to Pandas DateTime
df_weight['Date'] = pd.to_datetime(df_weight['Date'])

# Remove timezone information and floor dates to day
df_weight['Date'] = df_weight['Date'].dt.tz_localize(None).dt.floor('D')

# Set the date as index and sort
df_weight = df_weight.set_index('Date', drop = False).sort_index()

# Extract only MyFitnessPal entries. 
# Setup is currently such that MyFitnessPal reads data from Hevy
df_weight = df_weight.loc[df_weight['Source'] == 'MyFitnessPal']

# Drop duplicate entries
df_weight = df_weight.drop_duplicates()


# Weekly averages

# Move index into column
df_weight['Date'] = df_weight.index

# Create a new column containing the starting day of the week
df_weight['WeekStart'] = df_weight['Date'] - pd.to_timedelta(df_weight['Date'].dt.dayofweek, unit = 'd')

# Calculate the weekly average
weight_weekly = df_weight.groupby('WeekStart')['Weight'].mean()

# Convert Series to DataFrame
df_weight_weekly = pd.DataFrame({'Date':weight_weekly.index, 'Weight':weight_weekly.values})


# Today's date
today = datetime.date.today()

# Number of months past
nmonths = 6

# Get the date 6 months ago
six_months_ago = today - datetime.timedelta(days = 30*nmonths)

# Get entries after 6 months ago
weight_weekly_recent = weight_weekly.truncate(before = six_months_ago)

# Rebuild the weekly data frame
df_weight_weekly = pd.DataFrame({'Date':weight_weekly_recent.index,
                                 'Weight':weight_weekly_recent.values})

# Get min and max weights over the period
weight_min = min(df_weight_weekly['Weight'])
weight_max = max(df_weight_weekly['Weight'])

# Compute y-limits from min/max weights
ylim_min = math.floor(weight_min/5) * 5 
ylim_max = math.ceil(weight_max/5) * 5 

# Tick locator at every Monday
monday_loc = mdates.WeekdayLocator(byweekday = mdates.MO, interval = 1)

# Tick locator first day of each month
month_loc = mdates.MonthLocator(interval = 1)


# Weekly deltas --------------

# Compute weight differences successive rows
df_weight_diff = df_weight_weekly.diff().rename(columns = {'Date':'Timelapse', 'Weight':'Difference'})

# Concatenate weight difference data to weight averages
df_weight_diff = pd.concat([df_weight_weekly, df_weight_diff], axis = 1)

# Remove first entry (which is NA)
df_weight_diff = df_weight_diff[1:]


@render.plot(height = 600)
def plot_weekly_trends():

    fig, axes = plt.subplots(nrows = 2)

    # Generate the line plot
    lines = axes[0].plot('Date', 'Weight', data = df_weight_diff, lw = 0.80)
    points = axes[0].scatter('Date', 'Weight', data = df_weight_diff)


    # Set y-ticks and limits
    axes[0].set_yticks(np.arange(110, ylim_max+1, 1))
    axes[0].set_yticks(np.arange(110, ylim_min, 0.5), minor = True)
    axes[0].set_ylim(ylim_min, ylim_max)

    axes[1].bar('Date', 'Difference', 
        data = df_weight_diff,
        # color = bar_colors,
        align = 'center', 
        width = datetime.timedelta(days = 6))

    # Horizontal line at y = 0
    axes[1].axhline(y = 0, color = 'black')

    axes[1].set_xlim(axes[0].get_xlim())

    # ax.set_yticks(np.arange(-5, 6))
    # ax.set_yticks(np.arange(-5, 6, 0.5), minor = True)

    for ax in axes:
        ax.set_axisbelow(True)

        ax.xaxis.set_major_locator(month_loc)
        ax.xaxis.set_minor_locator(monday_loc)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        ax.grid(visible = True, which = 'major', color = '0.7')
        ax.grid(visible = True, which = 'minor', axis = 'both', color = '0.90')

        ax.set_ylabel("Weight (lbs)");


