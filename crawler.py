# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
from urlparse import urlsplit
import requests
import re
import sys
import urllib2


class Crawler(object):

    def __init__(self, urls):
        '''
        @urls: a string containing the (comma separated) URLs to crawl.
        '''
        self.urls = urls.split(',')


    def crawl(self):
        '''
        Iterate the list of URLs and request each page, then parse it and
        print the emails we find.
        
	'''

	mail = set()
	process_mail = set()
	tp = ['flv', 'jpg', 'docx', 'pdf']
	for url in self.urls:
		if "http" not in url:
			url = "http://" + url + "/"
		process_mail.add(url)
		parts = urlsplit(url)
		base_url = "{0.scheme}://{0.netloc}".format(parts)
		path = url[:url.rfind('/')+1] if '/' in parts.path else url
		
		data = self.request(url)
		'''
		for email in self.process(data):
			mail.add(email)
			mail = mail | mail
		'''
		soup = BeautifulSoup(data)
		for anchor in soup.find_all("a"):
        		# extract link url from the anchor
			link = anchor.attrs["href"] if "href" in anchor.attrs else ''

			# resolve relative links
        		if link.startswith('/'):
        			link = base_url + link
				#self.urls.append(link.encode("utf8").strip())
			elif not link.startswith('http'):
				#self.urls.append(link.encode("utf8").strip())
				link = path + link
			
	
			if link not in self.urls and link not in process_mail and len(self.urls)<=100:
				for t in tp:
					if t not in link:
						self.urls.append(link)

			
		#for web in re.findall(r'href=[\'"]?([^\'" >]+)',data):
		#	self.urls.append(web)
	
	for url in process_mail:
		data = self.request(url)
		for email in self.process(data):
			mail.add(email)
			mail = mail | mail        
	for i in mail:
		print i
	print len(mail)	
				
	
	
    @staticmethod
    def request(url):
        '''
        Request @url and return the page contents.
        '''
	
	try:
       		response = urllib2.urlopen(url)
   		return response.read()
	except:
		return ''
		

    @staticmethod
    def process(data):
        '''
        Process @data and yield the emails we find in it.
        '''
        for email in re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', data):
            yield email


def main():
    urls = sys.argv[1]
    '''
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--urls', dest='urls', required=True,
        help='A comma separated string of emails.')
    parsed_args = argparser.parse_args()
    '''
    crawler = Crawler(urls)
    crawler.crawl()


if __name__ == '__main__':
  sys.exit(main())
