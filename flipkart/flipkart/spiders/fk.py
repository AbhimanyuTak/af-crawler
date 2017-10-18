import scrapy
import sqlite3

# Creates or opens a file called crawler with a SQLite3 DB
db = sqlite3.connect('db/crawler.db')


def createTable():
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE flipkart(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
                           model TEXT, price FLOAT, added_on DATETIME, updated_on DATETIME);
        CREATE TABLE amazon(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
                           model TEXT, price FLOAT, added_on DATETIME, updated_on DATETIME);
    ''')
    db.commit()


class QuotesSpider(scrapy.Spider):
    name = "flipkart"
    total = 0

    def start_requests(self):
        urls = [
            'https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-front-load~function/pr?page=1&sid=j9e%2Cabm%2C8qx',
            'https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/semi-automatic-top-load~function/pr?page=1&sid=j9e%2Cabm%2C8qx',
            'https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-top-load~function/pr?page=1&sid=j9e%2Cabm%2C8qx',
            'https://www.flipkart.com/home-entertainment/televisions/pr?page=1&sid=ckf,czl&q=24-inches-led-tv',
            'https://www.flipkart.com/search?p%5B%5D=facets.screen_size%255B%255D%3D32&sid=ckf%2Fczl',
            'https://www.flipkart.com/search?p%5B%5D=facets.screen_size%255B%255D%3D39%2B-%2B43&sid=ckf%2Fczl',
            'https://www.flipkart.com/search?p%5B%5D=facets.screen_size%255B%255D%3D48%2B-%2B50&sid=ckf%2Fczl',
            'https://www.flipkart.com/search?p%5B%5D=facets.screen_size%255B%255D%3D55%2B%2526%2BAbove&sid=ckf%2Fczl',
            'https://www.flipkart.com/home-kitchen/home-appliances/refrigerators/single-door~type/pr?sid=j9e%2Cabm%2Chzg',
            'https://www.flipkart.com/home-kitchen/home-appliances/refrigerators/double-door~type/pr?sid=j9e%2Cabm%2Chzg',
            'https://www.flipkart.com/home-kitchen/home-appliances/refrigerators/triple-door~type/pr?sid=j9e,abm,hzg',
            'https://www.flipkart.com/home-kitchen/home-appliances/refrigerators/pr?p%5B%5D=facets.type%255B%255D%3DSide%2Bby%2BSide&sid=j9e%2Fabm%2Fhzg',
            'https://www.flipkart.com/home-kitchen/home-appliances/air-conditioners/split~type/pr?sid=j9e,abm,c54',
            'https://www.flipkart.com/home-kitchen/home-appliances/air-conditioners/window~type/pr?sid=j9e%2Cabm%2Cc54',
            'https://www.flipkart.com/microwave-ovens/pr?sid=j9e%2Cm38%2Co49&p=facets.type%255B%255D%3DConvection',
            'https://www.flipkart.com/microwave-ovens/pr?sid=j9e%2Cm38%2Co49&p=facets.type%255B%255D%3DSolo',
            'https://www.flipkart.com/microwave-ovens/pr?sid=j9e%2Cm38%2Co49&p=facets.type%255B%255D%3DGrill',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for quote in response.css('div._1-2Iqu'):
            # print model
            self.total += 1
            # print quote.css('.OiPjke::text').extract_first()
            print ("products fetched"),
            print self.total

            yield {
                'title': quote.css('._3wU53n::text').extract_first(),
                'price': quote.css('._1vC4OE::text')[1].extract(),
                'model': quote.css('.OiPjke::text').extract_first(),
            }

        nextText = response.css('._2kUstJ a span::text').extract()
        print nextText
        next_page_array =  response.css('._2kUstJ a::attr(href)').extract()
        if len(nextText) == 2:
            if(nextText[0].lower() == "next"):
                next_page = next_page_array[0]
            else: 
                next_page = next_page_array[1]
        else:
            if(nextText[0].lower() == "next"):
                next_page = next_page_array[0]
            else: 
                return

        next_page = "https://www.flipkart.com" + next_page

        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>" + next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)