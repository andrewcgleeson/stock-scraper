import scrapy
import os
from dotenv import load_dotenv
load_dotenv()

class StocksSpider(scrapy.Spider):
    name = "stocks"
    
    def start_requests(self):
        urls = [
            os.getenv('urls')
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath(f'//*[@id="maincontent"]/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/table/tbody//tr'):
            yield {
                'currency_name': row.xpath('td[1]/a/text()').get(),
                'current_value': row.xpath('td[2]/bg-quote/text()').get(),
            }