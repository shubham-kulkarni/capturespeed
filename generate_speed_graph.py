#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# Config
base_dir = "/home/pi/capturespeed"
log_dir = os.path.join(base_dir, "logs")
graph_dir = os.path.join(base_dir, "graphs")
os.makedirs(graph_dir, exist_ok=True)

# Get today's date
today = datetime.now()                    #- timedelta(days=1)      # Previous Days
date_str = today.strftime("%Y-%m-%d")

csv_path = os.path.join(log_dir, f"speedtest_{date_str}.csv")
image_path = os.path.join(graph_dir, f"speed_{date_str}.png")

# Check if CSV exists
if not os.path.exists(csv_path):
    print(f"[{date_str}] CSV not found, skipping.")
    exit()

df = pd.read_csv(csv_path)

if df.empty:
    print(f"[{date_str}] CSV is empty, skipping.")
    exit()

df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df.sort_values('Datetime', inplace=True)

plt.figure(figsize=(10, 5))
plt.plot(df['Datetime'], df['Download (Mbps)'], label='Download (Mbps)', color='red', marker='o')
plt.plot(df['Datetime'], df['Upload (Mbps)'], label='Upload (Mbps)', color='green', marker='o')

# Format x-axis to show only hour:minute
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#plt.gcf().autofmt_xdate()

ax = plt.gca()

if len(df) == 1:
    # Single data point — manually set tick to the exact time
    ax.set_xticks([df['Datetime'].iloc[0]])
    ax.set_xticklabels([df['Datetime'].iloc[0].strftime('%H:%M')])
else:
    # Multiple points — format as usual
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gcf().autofmt_xdate()


plt.xlabel('Time')
plt.ylabel('Speed (Mbps)')
plt.title(f'Internet Speed - {date_str}')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(image_path)
plt.close()

print(f"[{date_str}] Graph saved → {image_path}")

