import scrapy
import os
from dotenv import load_dotenv
load_dotenv()

class StocksSpider(scrapy.Spider):
    name = "stocks"
    
    start_urls = [os.getenv('urls')]

    def parse(self, response):
        # coin_page_links = response.xpath('//main[@id="maincontent"]/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/table/tbody//tr//a').attrib['href']
        # yield from response.follow(coin_page_links, callback=self.parse_pages)
        for href in response.xpath('//main[@id="maincontent"]/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/table/tbody//tr//a/@href'):
            url=response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_pages)
    
    def parse_pages(self, response):
        def extract_information(query):
            return response.xpath(query).get()
        
        yield {
            'coin_name': extract_information('//*[@id="maincontent"]/div[1]/div[2]/div/div[2]/h1/text()'),
            'current_price': extract_information('//*[@id="maincontent"]/div[1]/div[3]/div/div[2]/h2/bg-quote/text()'),
            'day_change': extract_information('//*[@id="maincontent"]/div[1]/div[3]/div/div[2]/bg-quote/span[2]/bg-quote/text()')
        }