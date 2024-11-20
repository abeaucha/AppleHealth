import datetime
import math
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from shiny.express import render, ui

# Data directory
data_dir = 'data'

# Data file
file = 'AppleHealth_BodyMass.csv'
file = os.path.join(data_dir, file)
if not os.path.exists(file):
    raise ValueError

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

# Recent entries
# df_weight[['Weight']].tail(n = 7).sort_values(by = 'Date', ascending = False)


# I'm not sure how this works. 
with ui.card(full_screen = True):
    ui.card_header("Test")
    @render.data_frame
    def table():
        return render.DataGrid(df_weight[['Weight']].tail(n = 7).sort_values(by = 'Date', ascending = False))
    # @render.data_frame
    # def table():
    #     return render.DataGrid(tips_data())