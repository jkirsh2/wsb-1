import praw
import time
import datetime


def string_to_unix(s, format):
    return time.mktime(datetime.datetime.strptime(s, format).timetuple())



class SubScraper:
    def __init__(self, cred_file):
        with open(cred_file, 'r') as f:
            creds = [x.strip() for x in f]

        self.R = praw.Reddit(client_id=creds[0],
                             client_secret=creds[1],
                             password=creds[2],
                             user_agent='testscript by ya boi',
                             username='wsbIndex')

    def get_submissions_between(self, subreddit, start_date, end_date):
        sdate_unix = string_to_unix(start_date, '%Y-%M-%d')
        edate_unix = string_to_unix(end_date, '%Y-%M-%d')
        submissions = self.R.subreddit(subreddit).submissions(sdate_unix, edate_unix)
        return submissions


if __name__ == "__main__":
    s = SubScraper('/home/andrew/gitrepos/wsb/RETF/credentials.txt')
    submissions = s.get_submissions_between('wallstreetbets', '2017-01-01', '2017-01-02')

	for submission in submissions:
		try:
			p =  post(
					rid = submission.id
					,created = submission.created
					,author = str(submission.author)
					,title = submission.title
					,selftext = str(submission.selftext.decode('utf-8'))
					,num_comments = submission.num_comments
					,score = submission.score
					)

			db.session.add(p)
			db.session.commit()
		except Exception,e:
			print str(e)
			pass

		submission.comments.replace_more(limit=0)
		for comm in submission.comments.list():
			try:
				c = comment(
					rid = comm.id
					,created = comm.created
					,author = str(comm.author)
					,body = str(comm.body.decode('utf-8'))
					,score = comm.score
					,original_post = p
					)
				db.session.add(c)
				db.session.commit()
			except Exception,e:
				print str(e)
				pass

