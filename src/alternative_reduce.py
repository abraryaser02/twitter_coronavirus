#!/usr/bin/env python3

# command line args
import argparse
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from collections import defaultdict
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--hashtags',nargs='+',required=True)
args = parser.parse_args()

# Get current working directory
current_directory = os.getcwd() 
outputs_directory = os.path.join(current_directory, "outputs")
outputs_path = os.path.normpath(outputs_directory)

# load each of the input paths

hashtag_totals = defaultdict(lambda: defaultdict(int))

for filename in os.listdir(outputs_path):
    if filename.endswith('.zip.lang'):
        date_str = filename[10:18]
        date_object = datetime.strptime(date_str, '%y-%m-%d')
        day_of_year = date_object.timetuple().tm_yday
        
        file_path = os.path.join(outputs_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            for hashtag in args.hashtags:
                if hashtag in data:
                    total = int(sum(data[hashtag].values()))
                    hashtag_totals[hashtag][day_of_year] += total

# plot

korean_path = '/home/ayaa2021/twitter_coronavirus/fonts/NotoSansKR-SemiBold.ttf'
font = FontProperties(fname=korean_path)
plt.figure(figsize=(12, 8))

for hashtag in args.hashtags:
    days = sorted(hashtag_totals[hashtag].keys())
    counts = [hashtag_totals[hashtag][day] for day in days]
    print(days)
    print(counts)

    plt.plot(days, counts, label=hashtag, marker='x')

plt.legend()

plt.xlabel('Day of the Year', fontproperties=font)
plt.ylabel('Number of Tweets', fontproperties=font)

# Ensure the images folder exists
images_folder = os.path.join(os.path.expanduser('~'), 'twitter_coronavirus', 'images')
os.makedirs(images_folder, exist_ok=True)

output_path = os.path.join(images_folder, f'{args.hashtags}_counts.png')
plt.savefig(output_path)
plt.show()
plt.close()

