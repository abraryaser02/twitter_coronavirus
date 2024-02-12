#!/usr/bin/env python3

# command line args
import os
import re
import json
import matplotlib 
matplotlib.use('Agg')
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
import matplotlib.pyplot as plt
from collections import Counter,defaultdict
from matplotlib.font_manager import FontProperties

# Customize font settings

font_path = '/home/ayaa2021/twitter_coronavirus/fonts/NotoSerif-SemiBold.ttf'
korean_path = '/home/ayaa2021/twitter_coronavirus/fonts/NotoSansKR-SemiBold.ttf'

korean_pattern = re.compile('[ㄱ-ㅎ가-힣]')
if korean_pattern.search(args.key):
    font = FontProperties(fname=korean_path)
else:
    font = font = FontProperties(fname=font_path)

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# sort the current values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)[:10]
items = reversed(items)
keys, values = zip(*items)

# plot the graph

plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.xlabel(args.key, fontproperties=font)
plt.ylabel('Tweet Count' if not args.percent else 'Percentage', fontproperties=font)
plt.title(f'Top 10 {args.key} Counts' + (' (Percentage)' if args.percent else ''), fontproperties=font)
plt.xticks(rotation=45, ha='right', fontstyle='italic', fontproperties=font)
plt.tight_layout()

# Ensure the images folder exists
images_folder = os.path.join(os.path.expanduser('~'), 'twitter_coronavirus', 'images')
os.makedirs(images_folder, exist_ok=True)

# Save the plot to a PNG file in the images folder
output_path = os.path.join(images_folder, f'top_10_{args.key}_counts.png')
plt.savefig(output_path)

# Show the plot
plt.show()
plt.close()

if args.percent:
    for key, value in items:
        print(f"{key}: {value*100:.2f}%")
else:
    for key, value in items:
        print(f"{key}: {value}")
