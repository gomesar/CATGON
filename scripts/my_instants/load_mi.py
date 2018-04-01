#!/usr/bin/python
#coding: utf-8

# 
# Runs a scrapper to index the urls of all MyInstant's audios
# Outputs goes to output.json
# 
import scrapy
from bs4 import BeautifulSoup
import re

class MyInstants(scrapy.Spider):
	name = 'myinstantsspider'
	start_urls = ['https://www.myinstants.com/index/br/?page=1']

	def parse(self, response):
		for instant in response.xpath('//*[@id="instants_container"]/div'):
			data = instant.css('div.small-button').extract_first()
			link = instant.css('a').extract_first()
			if data is not None:
				soup = BeautifulSoup(data, 'html.parser')
				url = "https://www.myinstants.com" + re.search( "(?<=play\(\').*" , soup.div["onmousedown"]).group(0)[:-2]
				
				soup = BeautifulSoup(link, 'html.parser')
				title = soup.text
				
				yield {'url': url, "title": title}

		# follow next page links
		next_page = response.xpath('//*[@id="content"]/ul/li/a[@rel="next"]/@href').extract()
		if next_page:
			self.log(next_page[0])
			next_url = "https://www.myinstants.com/index/br/" + next_page[0]
			request = scrapy.Request(url=next_url, dont_filter=True)
			yield request