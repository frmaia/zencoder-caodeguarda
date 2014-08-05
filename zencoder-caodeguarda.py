#!/usr/bin/python

import argparse
import dateutil.parser
import json
import requests
import sys
import urllib2

from datetime import datetime, timedelta


def getZencoderNotifications(api_key, since, page=1, per_page=50):

	req_headers = {"Zencoder-Api-Key": api_key}

	req_url = "https://app.zencoder.com/api/v2/notifications.json?since=%s&page=%s&per_page=%s" % (since,page,per_page)
	
	req = urllib2.Request(req_url, headers = req_headers)
	response_str = urllib2.urlopen(req).read()
	return json.loads(response_str)

def printNotification(notification, verbose=False):

		job_id = notification['job']['id']
		output_fname = notification['output']['url'].split('/')[-1].split('?')[0]
		print "##### job_id = %s -- output_file_name = %s" % ( notification['job']['id'] , output_fname )
		if verbose:
			print "#"*50
			print "%s" % json.dumps(notification)
			print "#"*50

def postNotifications(notifications_to_post, url_to_post, verbose):
	headers = {'Content-type': 'application/json'}
	for n in notifications_to_post:
		print "Posting to '%s'..." % url_to_post
		printNotification(n, verbose)
		r = requests.post(url_to_post, data=json.dumps(n), headers=headers)
		print "Status code = %s" % r.status_code
		print "/"*50


def processNotifications(notifications, jobs_filter, file_name_filter, url_to_post, list_only, verbose):

	# Interpret args and process API query result
	notifications_to_post = []
	if jobs_filter:
		for n in notifications:
			if str(n['job']['id']) in jobs_filter:
				notifications_to_post.append(n)

	elif file_name_filter:

		for n in notifications:
			if file_name_filter in n['output']['url']:
				notifications_to_post.append(n)	
	else:
		#Get all...
		for n in notifications:
			notifications_to_post.append(n)

	#Print or resend notifications...
	if url_to_post:
		postNotifications(notifications_to_post, url_to_post, verbose)
	elif list_only:
		for n in notifications_to_post:
			printNotification(n, verbose)
		

def main(args):

	usage = """
		Usage Example: 
			python zencoder-caodeguarda.py --api_key={Zencoder API Key} --since="2013-08-07T22:27:00Z" --filterByOutputFileName=policia_rouba.mp4 --verbose --postToUrl=http://requestb.in/105jpxg1
			"""

	#Args parser...
	parser=argparse.ArgumentParser(
	    description='''Customized Zencoder notifications fetcher to help you in dev of integration tasks!''')
	parser.add_argument('--api-key', help='Zencoder API Key', required=True, dest='api_key')
	#parser.add_argument('--since', help="UTC Datetime in iso8601 format (example: '2013-08-01T20:00:00Z'", required=True)
	parser.add_argument('--since-minutes', help="All jobs created after this value will be evaluated", required=True, dest='since_minutes', type=int)

	parser.add_argument('--filter-jobs', help="Optionally filter comma sepparated Zencoder Job ID's", required=False, dest='filter_jobs')
	parser.add_argument('--filter-filename', help="Optionally filter only jobs in which the filename is used", required=False, dest='file_name_filter')

	parser.add_argument('--list-only', help="Only List notifications sent since <sent_since> period", required=False, default=True, dest='list_only', type=bool)
	parser.add_argument('--verbose', help="Print notifications in JSON format", required=False, action='store_true' )
	parser.add_argument('--post-to-url', help="Define an URL in which the fetched messages will be automatically posted (HTTP POST request)", required=False, dest='url_to_post')

	args=parser.parse_args()

	api_key = args.api_key

	since_dt = datetime.utcnow() - timedelta(minutes=args.since_minutes)
	since = since_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

	jobs_filter = args.filter_jobs
	if jobs_filter is not None:
		jobs_filter = jobs_filter.split(',')
	file_name_filter = args.file_name_filter
	url_to_post = args.url_to_post
	list_only = args.list_only
	verbose = args.verbose	
	
	
	# Get API query result
	page = 1
	r = getZencoderNotifications(api_key, since, page=page, per_page=50)
	notifications = r['notifications']
	while len(notifications) > 0:
		processNotifications(notifications, jobs_filter, file_name_filter, url_to_post, list_only, verbose)

		page += 1
		r = getZencoderNotifications(api_key, since, page=page, per_page=50)
		notifications = r['notifications']

if __name__ == '__main__':
	main(sys.argv[1:])

