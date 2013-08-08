zencoder-caodeguarda
====================

A Zencoder notifications fetcher written in Python!

```
usage: zencoder-caodeguarda.py [-h] --api_key API_KEY --since SINCE
                               [--filterByJobs FILTERBYJOBS]
                               [--filterByOutputFileName FILTERBYOUTPUTFILENAME]
                               [--listOnly LISTONLY] [--verbose]
                               [--postToUrl POSTTOURL]

Customized Zencoder notifications fetcher to help you in dev of integration
tasks!

optional arguments:
  -h, --help            show this help message and exit
  --api_key API_KEY     Zencoder API Key
  --since SINCE         UTC Datetime in iso8601 format (example:
                        '2013-08-01T20:00:00Z'
  --filterByJobs FILTERBYJOBS
                        Filter by jobs.
  --filterByOutputFileName FILTERBYOUTPUTFILENAME
                        Filter By OutputfileName
  --listOnly LISTONLY   Only List notifications sent since <sent_since> period
  --verbose             Print notifications in JSON format
  --postToUrl POSTTOURL
                        Filter By OutputfileName
                        
  
  
usage Example: 

			python zencoder-caodeguarda.py --api_key={Zencoder API Key} --since="2013-08-07T22:27:00Z" --filterByOutputFileName=policia_rouba.mp4 --verbose --postToUrl=http://requestb.in/105jpxg1

  
```                      
