import scrapy
from bs4 import BeautifulSoup
from test.items import Images
from lxml import etree
from selenium import webdriver
from urllib import FancyURLopener

browser = webdriver.Firefox()

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


class DmozSpider(scrapy.Spider):
    name = "test"
    
    start_urls = [
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-front-" +
                    "load~function/pr?sid=j9e%2Cabm%2C8qx&page=1",
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-front-" +
                    "load~function/pr?sid=j9e%2Cabm%2C8qx&page=2",
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/semi-automatic-top-load~"+
                    "function/pr?sid=j9e%2Cabm%2C8qx&page=1",
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/semi-automatic-top-load~"+
                    "function/pr?sid=j9e%2Cabm%2C8qx&page=2",
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/semi-automatic-top-load~"+
                    "function/pr?sid=j9e%2Cabm%2C8qx&page=3",
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-top-load~f"+
                    "unction/pr?sid=j9e%2Cabm%2C8qx&page=1",
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-top-load~f"+
                    "unction/pr?sid=j9e%2Cabm%2C8qx&page=2",
                    "https://www.flipkart.com/home-kitchen/home-appliances/washing-machines/fully-automatic-top-load~f"+
                    "unction/pr?sid=j9e%2Cabm%2C8qx&page=3"
                     ]
    
    def start_requests(self):
        self.logger.debug("Starting the crawling")
        for url in self.start_urls:
            # browser.get(url, callback = self.parse,endpoint='render.html', args = {'wait': 0.5,'script':1})
            browser.get(url)

            # print browser
            # assert "Fully" in browser.title
            elem = browser.find_elements_by_class_name("_3wU53n")
            # print elem
            

    def parse(self, response):
        self.logger.debug("Response: status=%d; url=%s" % (response.status, response.url))
        #self.logger.debug(response.body)
        page_body = BeautifulSoup(response.body)
        allProducts = page_body.find_all('div',class_="_2xw3j-")
        links = allProducts[0].find_all('a',class_= "_1UoZlX")
        
        for link in links:
            next_page = 'https://www.flipkart.com' + link['href']
            if next_page :
                yield browser.get(next_page, callback=self.parseProductPage, endpoint='render.html',
                    args = {'wait': 5,
                    'script':1})
        
    def     parseProductPage(self,response):

        self.logger.debug("Response: status=%d; url=%s" % (response.status, response.url))
        page_body = BeautifulSoup(response.body)

        nameDiv = page_body.find('div',class_='_2UDlNd')
        prodName = nameDiv.find('h1',class_='_3eAQiD').getText()

        product_li = page_body.find_all('li',class_ = '_4f8Q22 _1WPMdP')
        i = 0

        for li in product_li :
            d = li.find('div',class_ = '_1kJJoT')
            image_url = d['style'].split('url(')[1].split(')')[0].replace('128','832').replace("'","").replace('?q=70','')
            
            if image_url :
                item = Images()
                item['image_product_name'] = prodName
                item['image_url'] = image_url
                #myopener = MyOpener()
                #myopener.retrieve(image_url,prodName + str(i) +'.jpeg')
                i = i + 1
                self.logger.debug("Image Url is %s"%(image_url))
                yield item

