import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-front-load~function/pr?sid=j9e%2Cabm%2C8qx'
    ]

    def parse(self, response):
        for quote in response.css('div._1-2Iqu'):
            print "quote"
            print quote
            yield {
                'text': quote.css('_3wU53n').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
