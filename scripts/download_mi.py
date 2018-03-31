#!/usr/bin/python3
#coding: utf-8

# 
# Loads data from output.json and downloads all files to data/
# 

from clint.textui import progress
import json
import math
import random
import threading
import requests
from time import sleep

# You must define a proxy list
# I suggests https://free-proxy-list.net/
proxies = {
	0: {'http': 'http://34.208.47.183:80'},
	1: {'http': 'http://40.69.191.149:3128'},
	2: {'http': 'http://104.154.205.214:1080'},
	3: {'http': 'http://52.11.190.64:3128'}
}

def downloaders(package, selected_proxy):
	url = package["url"]
	filename = package["title"]

	print("Downloading file named {} by proxy {}...".format(package, selected_proxy))
	r = requests.get(url, stream=True, proxies=selected_proxy)
	with open("data/" + filename + ".mp3", 'wb') as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
			if chunk:
				f.write(chunk)
			f.flush()

# Load output.json
with open("output.json") as f:
	videos = json.load(f)

	downloaderses = list()

	for video in videos:
		selected_proxy = proxies[math.floor(random.random() * len(proxies))]
		t = threading.Thread(target=downloaders, args=(video, selected_proxy))
		downloaderses.append(t)

	count = 0
	for _downloaders in downloaderses:
		_downloaders.start()
		count += 1

		# There is an upper bound for the number of active threads
		# This is a temporary solution
		if count % 30 == 0:
			sleep(5)

