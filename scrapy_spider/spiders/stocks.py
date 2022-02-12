import scrapy
import os
from dotenv import load_dotenv
load_dotenv()

class StocksSpider(scrapy.Spider):
    name = "stocks"
    
    start_urls = [os.getenv('urls')]

    def parse(self, response):
        for href in response.xpath('//table/tbody//tr//a[@class="link"]/@href'):
            url=response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_pages)
    
    def parse_pages(self, response):
        def extract_information(query):
            return response.xpath(query).get()
        
        yield {
            'coin_name': extract_information('//h1[@class="company__name"]/text()'),
            'current_price': '$' + extract_information('//*[@id="maincontent"]//h2/bg-quote/text()'),
            'day_change': extract_information('//span[@class="change--percent--q"]//bg-quote[1]/text()'),
            'five_day_change': extract_information('//table/tbody/tr[1]/td[2]/ul/li[1]/text()'),
            'one_month_change': extract_information('//table/tbody/tr[2]/td[2]/ul/li[1]/text()'),
            'one_year_change': extract_information('//table/tbody/tr[5]/td[2]/ul/li[1]/text()')
        }