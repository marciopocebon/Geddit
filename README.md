# Geddit

Download imgur images/galleries from a sub-reddit

## Description

Given the name of a sub-reddit, download
It will download the individual image or it will download and unzip the entire gallery. It accepts a number as the second parameter to specify how many images to download. The default is 10, but the maximum is only limited by the Reddit API (100 max). The images are downloaded
to a subfolder with the name of the subreddit. Written in Python 3.

## Usage

	python geddit.py <subreddit_name> [limit]

## Example usage

	python geddit.py awww 3
	python geddit.py adviceanimals 100