## Reddit Scraper

#### Notes

* API rate limit of 30 calls per minute
* Posts come with top-level comments. Each additional level requires an API call
* Credentials file has 3 lines, client_id, client_secret, and password respectively (no quotes)
* Run like so: `andrew@mycomputer:~/gitrepos/wsb/dev/scraper_nodb$ python run.py`