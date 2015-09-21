#!/bin/env python
import sys
import urllib.request
import json
import os
import zipfile
import shutil

# Fail if no subreddit name provided
if len(sys.argv) < 2:
	print("Not enough arguments. Pass in a subreddit name and optionally a count (default 10).")
	print("Example: ")
	print("python geddit.py adviceadnimals")
	print("python geddit.py awww 50")
	exit(1)
else:
	subreddit = sys.argv[1]

if len(sys.argv) > 2:
	limit = sys.argv[2]
else:
	limit = 10
	
# URL for new posts with max limit of 100
reddit_url = "http://www.reddit.com/r/" + subreddit + ".json?limit=" + str(limit)

# Get JSON and convert items to object
request = urllib.request.Request(reddit_url, headers={"User-Agent":"Geddit Bot v0.0"})
subreddit_json = urllib.request.urlopen(request).read().decode()
data = json.loads(subreddit_json)
items = data['data']['children']

# Go through each post and find imgur links, and create download URL
for item in items:

	url = item['data']['url']

	if not "imgur.com" in url: continue

	# Remove hash to end of url if # is present
	hash_index = url.find("#")
	if hash_index != -1:
		url = url[0:hash_index]

	# Remove hash to end of url if # is present
	q_index = url.find("?")
	if q_index != -1:
		url = url[0:q_index]

	# Generate download url and download file name
	split_url = url.split("/")
	if any(ext in url for ext in [".jpg", ".png", ".gif"]):
		dl_url = url
		filename = split_url[-1]
	else:
		# If path is /x/asdfasdf it's a gallery, add /zip
		# /asdfasdf it's just a single image, add .jpg
		parsed_url = urllib.parse.urlparse(url)
		split_path = parsed_url.path.split("/")
		if len(split_path) > 2:
			dl_url = url + "/zip"
			filename = split_url[-1] + ".zip"
		else:
			dl_url = url + ".jpg"
			filename = split_url[-1] + ".jpg"

	# Transform simple file name into download path ./subreddit/filename.xxx
	dl_filename = os.path.join(os.getcwd(), subreddit, filename)
	if os.path.isfile(dl_filename): continue

	# If subreddit folder does not exist, create it
	if not os.path.isdir(subreddit): os.mkdir(subreddit)

	# Download file	
	try:
		#print("Trying to retreive " + dl_url + " to file: " + dl_filename)
		urllib.request.urlretrieve(dl_url, dl_filename)
	except:
		print("** Error trying to download: " + dl_url)
		continue

	# Unzip and remove zip file if it is an archive
	if ".zip" in filename:
		fh = open(dl_filename, 'rb')
		try:
			zipped_file = zipfile.ZipFile(fh)
		except:
			print("** Error trying to open zip file: " + dl_filename)
			#print("Unexpected error:", sys.exc_info()[0])
			fh.close
			try:
				os.remove(dl_filename)
			except:
				print("Failed to remove zip file: " + dl_filename)
			"""
			# Create "broken_zips" directory and move errored zips there
			if not os.path.isdir(
					os.path.join(subreddit, "broken_zips")):
				os.mkdir(os.path.join(subreddit, "broken_zips"))
			shutil.move(dl_filename, os.path.join(
				os.getcwd(), subreddit, "broken_zips", filename))
			"""
			continue
		for f in zipped_file.namelist():
		    if f.endswith('/'):
		        os.makedirs(f)
		outpath = os.path.join(os.getcwd(), subreddit)
		zipped_file.extractall(outpath)
		zipped_file.close
		fh.close
		try:
			os.remove(dl_filename)
		except:
			print("Failed to remove: " + dl_filename)
	# url must contain imgur.com
	# if there is a # in it, strip it and everything to the right
	# split url, if last item does not contain .jpg, .jpeg, .gif, .png, 
		# assume it's a gallery and append .zip to it 

	
