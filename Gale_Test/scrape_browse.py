import requests
import MySQLdb
import json
from lxml import html
import sys,getopt
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')

class ScrapeContent:
	def __init__(self):
		print "Scraper"
		self.mysqldb_connection = MySQLdb.connect(host="localhost",user = "root", passwd="root", db="GALE_TEST")
		self.cur = self.mysqldb_connection.cursor()
		#self.cur = self.conn.cursor()
		self.insert_query = 'insert ignore into app_crawl_data(requested_url,image,crawled_from_url,depth_level,created_at,modified_at) values(%s,%s,%s,%s,now(),now())'

	def __del__(self):
		self.mysqldb_connection.commit()
		self.cur.close()
		self.mysqldb_connection.close()
		#self.conn.close()

	def main(self):
		print "Main"
		from optparse import OptionParser
        	parser = parser = OptionParser()
		parser.add_option("-u", "--url")
		parser.add_option("-d","--depth_level")

		options, args = parser.parse_args()
		self.url = str(options.url)
		self.depth_level_requested = int(options.depth_level)

		#self.depth_level_requested = 2 
		self.depth_count = 1
		self.start_url = start_url = [self.url]
		links = self.crawl(start_url)
		if self.depth_count<=self.depth_level_requested:
			if links:
				self.crawl(links)
			else:
				print "no links found"
		else:
			print "Done"

	def crawl(self,urls):
		domain = self.url.replace("https://",'').replace('http://','').split('/')[0]
		print "domain:%s"%domain
		for url in set(urls):
			data = requests.get(url)
			source = html.fromstring(data.text)
			images = set(source.xpath('//@data-desktop-image') + source.xpath('//img[not(contains(@src,".svg"))]/@src'))
			for image in images:
				image = image
				if image.startswith('https'):
					image = image
				else:
					if 'http://' in self.url:
						image = 'http://%s%s'%(domain,image)
					elif 'https://' in self.url:
						image = 'https://%s%s'%(domain,image)
				url = url
				self.depth_count = self.depth_count
				insert_values = (''.join(self.start_url),image,url,self.depth_count)

				self.cur.execute(self.insert_query,insert_values)
				
			links = set(source.xpath('//a[contains(@href,"%s")][contains(@href,"https")]/@href'%domain)) - set(urls)	
		self.depth_count = self.depth_count + 1
		return links

if __name__=="__main__":
	ScrapeContent().main()
