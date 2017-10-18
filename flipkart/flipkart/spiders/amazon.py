import scrapy
from urllib import urlencode
from urlparse import parse_qs, urlsplit, urlunsplit
import time

def set_query_parameter(url, param_name, param_value):
    """Given a URL, set or replace a query parameter and return the
    modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


class QuotesSpider(scrapy.Spider):
    name = "amazon"
    count = 0

    def start_requests(self):
        # urls = [
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md1_w?node=13829863031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md2_w?node=13829865031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md3_w?node=13829867031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md4_w?node=13829866031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LAWMSEO_md1_w?node=13829830031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LAWMSEO_md2_w?node=13829832031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LAWMSEO_md3_w?node=13829831031',
        #     'https://www.amazon.in/s/ref=s9_acss_bw_cg_headerT1_md3_w?rh=i%3Aelectronics%2Cn%3A976419031%2Cn%3A%21976420031%2Cn%3A1389375031%2Cn%3A1389396031%2Cp_n_feature_three_browse-bin%3A1485062031'
        # ]

         #Refs
        # urls = [
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md1_w?node=13829863031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md2_w?node=13829865031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md3_w?node=13829867031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LARef_md4_w?node=13829866031',
        # ]

        # Wms
        # urls = [
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LAWMSEO_md1_w?node=13829830031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LAWMSEO_md2_w?node=13829832031',
        #     'https://www.amazon.in/b/ref=s9_acss_bw_cg_LAWMSEO_md3_w?node=13829831031'
        # ]

        urls = [
            'https://www.amazon.in/b/ref=s9_acss_bw_cg_LAWMSEO_md1_w?node=13829830031'
        ]

        # # TV
        # urls = [
        #     'https://www.amazon.in/s/ref=s9_acss_bw_cg_headerT1_md3_w?rh=i%3Aelectronics%2Cn%3A976419031%2Cn%3A%21976420031%2Cn%3A1389375031%2Cn%3A1389396031%2Cp_n_feature_three_browse-bin%3A1485062031'
        # ]

        # # AC
        # urls = [
        #     'https://www.amazon.in/Air-Conditioners/b?node=3474656031'
        # ]

        # #MWO
        # urls = [
        #     'https://www.amazon.in/Microwave-Ovens/b/ref=sn_gfs_co_hk_1380072031_4?node=1380072031'
        # ]


        for url in urls:
            count = 0
            yield scrapy.Request(url=url, callback=self.parse, meta={'dont_merge_cookies': True})


    def parse(self, response):

        atf = len(response.css('#atfResults'))
        main = len(response.css('#mainResults'))

        if atf == 1:
            for prod in response.css('#atfResults .s-result-item'):
                productUrl = prod.css('a.s-access-detail-page::attr(href)').extract_first()
                yield scrapy.Request(productUrl, callback=self.getProductInfo)

        elif main == 1:
            for quote in response.css('#mainResults .s-item-container'):
                productUrl = quote.css('a.s-access-detail-page::attr(href)').extract_first()
                yield scrapy.Request(productUrl, callback=self.getProductInfo, meta={'dont_merge_cookies': True})
        else:
            print "CRAWLING NOT POSSIBLE"


        next_page = response.css('.pagnRA a::attr(href)').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print next_page
    
            yield scrapy.Request(next_page, callback=self.parse, meta={'dont_merge_cookies': True})


    def getProductInfo(self, response):
        # features = response.css('#prodDetails table tbody tr td::text').extract()
        # print features

        priceArr = response.css('#priceblock_ourprice::text')

        if len(priceArr) == 0:
            price = "NA"
        else:
            price = priceArr.extract_first().strip()

        yield {
            'title': response.css('span#productTitle::text').extract_first().strip(),
            'price': price,
            'model': response.css('#prodDetails table tbody tr td::text').extract()[3].strip()
        }
