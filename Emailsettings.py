import pandas as pd
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from lxml import html
from scrapy.crawler import CrawlerProcess

emails = pd.read_csv('SPOILER_imap-pop3.txt', header=None, names=['Name', 'Domain', 'Password'], sep='@|:', engine='python') # Load data without headers. Set up engine='python', because we need to use multiple separators to separate Domain from the Name.
domains = list(set(emails['Domain'].tolist())) # Retrun only unique values to get rid of dubbes.
urls = [f'https://www.emailsettings.email/search/pop3-imap-smtp-{i}-email-settings' for i in domains] # Create urls for unique domains.

class DataRowItem(scrapy.Item):  # Scrapy settings
    serverhostname = scrapy.Field()
    serverport = scrapy.Field()
    ssltsl = scrapy.Field()
    domain = scrapy.Field()
    type = scrapy.Field()
class DataRowItemLoader(scrapy.loader.ItemLoader):

    default_item_class = DataRowItem
    default_output_processor = TakeFirst()

class ImapSpider(scrapy.Spider): # Imap spider settings.
    name='spider'
    start_urls = urls
    #rate = 1                 ----Uncomment to set up rate for scraping

    #def __init__(self):
        #self.download_delay = 1/float(self.rate)

    def parse(self, response): # Method for extracting IMAP-values
        loader = DataRowItemLoader(DataRowItem(), response=response)
        loader.add_xpath('domain', '//td[@id="imap-username"]/text()')
        loader.add_xpath('serverhostname', '//td[@id="imap-hostname"]/text()')
        loader.add_xpath('serverport', '//td[@id="imap-port"]/text()')
        loader.add_xpath('ssltsl', '//td[@id="imap-secure"]/text()')
        loader.add_value('type', 'IMAP')

        yield loader.load_item()

class PopSpider(scrapy.Spider): # Pop3 spider settings.
    name='spider'
    start_urls = urls
    #rate = 1                ----Uncomment to set up rate for scraping

    #def __init__(self):
        #self.download_delay = 1/float(self.rate)

    def parse(self, response): # Method for extracting Pop3-values
        loader = DataRowItemLoader(DataRowItem(), response=response)
        loader.add_xpath('domain', '//td[@id="pop3-username"]/text()')
        loader.add_xpath('serverhostname', '//td[@id="pop3-hostname"]/text()')
        loader.add_xpath('serverport', '//td[@id="pop3-port"]/text()')
        loader.add_xpath('ssltsl', '//td[@id="pop3-secure"]/text()')
        loader.add_value('type', 'POP3')

        yield loader.load_item()

c = CrawlerProcess({ #CrawlerProcess settings to save excracted data.
    'USER_AGENT': 'Chrome/72.0.3626.119',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'set.txt',
    })
c.crawl(ImapSpider)
c.crawl(PopSpider)
c.start()
