#!/usr/bin/python

import argparse
import dateutil.parser
import json
import requests
import sys
import urllib2


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

def postNotifications(notifications_to_post, url_to_post):
	headers = {'Content-type': 'application/json'}
	for n in notifications_to_post:
		print "Posting to '%s'..." % url_to_post
		printNotification(n)
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
		postNotifications(notifications_to_post, url_to_post)
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
	parser.add_argument('--api_key', help='Zencoder API Key', required=True)
	parser.add_argument('--since', help="UTC Datetime in iso8601 format (example: '2013-08-01T20:00:00Z'", required=True)

	parser.add_argument('--filterByJobs', help="Filter by jobs.", required=False)
	parser.add_argument('--filterByOutputFileName', help="Filter By OutputfileName", required=False)

	parser.add_argument('--listOnly', help="Only List notifications sent since <sent_since> period", required=False, default=True)
	parser.add_argument('--verbose', help="Print notifications in JSON format ", required=False, action='store_true')
	parser.add_argument('--postToUrl', help="Filter By OutputfileName", required=False)

	args=parser.parse_args()

	api_key = args.api_key
	since_str = args.since

	jobs_filter = args.filterByJobs
	if jobs_filter is not None:
		jobs_filter = jobs_filter.split(',')
	file_name_filter = args.filterByOutputFileName
	url_to_post = args.postToUrl
	list_only = args.listOnly
	verbose = args.verbose	


	try: 
		since_dt = dateutil.parser.parse(since_str)
		since = since_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
	except ValueError, e:
		exit("You must specify a correct parameter for '--since'.")

	
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

