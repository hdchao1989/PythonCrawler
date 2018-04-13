from scrapy.spiders import Spider
from scrapytest.items import  ScrapytestItem
from scrapy import Request

class DoubanMovieTop250Spider(Spider):
    name = 'douban_book_top250'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://book.douban.com/top250'
        yield Request(url,headers = self.headers)

    def parse(self,response):
        item = ScrapytestItem()
        books = response.xpath('//tr[@class="item"]')
        for book in books:
            #item['ranking'] = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
            item['book'] = book.xpath('.//div[@class="pl2"]/a/@title').extract()[0]
            item['score'] = book.xpath('.//div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract()[0]
            item['score_num'] = book.xpath('.//div[@class="star clearfix"]/span[@class="pl"]/text()').re(r'(\d+)人评价')[0]
            item['quote'] = book.xpath('.//p[@class="quote"]/span[@class="inq"]/text()').extract()[0]
            item['author'] = book.xpath('.//p[@class="pl"]/text()').extract()[0].split("/")[0].strip()
            #item['author'] =  item['author'].spilt("/")[0]
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            yield Request(next_url[0],headers=self.headers)