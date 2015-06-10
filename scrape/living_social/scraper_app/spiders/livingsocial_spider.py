from scrapy.spider import BaseSpider
#deals with response of when we request webpage
#and gives us ability to select certain parts of response
from scrapy.selector import HtmlXPathSelector 
#used to load data into our item_fields
from srapy.contrib.loader import XPathItemLoader
#MapCompose helps with inputprocessing of the data
#used to help clean up data we extract
from scrapy.contrib.loader.processor import  MapCompose
#Join helps with output processing of data
#will join together elements that we process
from scrapy.contrib.loader.processor import Join

from scraper_app.items import LivingSocialDeal

class LivingSocialSpider(BaseSpider):
  """Spider for regularly updated livingsocial.com site, SF Page"""
  name = 'livingsocial'
  allowed_domains = ['livingsocial.com']
  #scrapy makes scrapy.http.Request objects for each URL in the start_urls attrib of the spider
  #and assigns them the parse method of the spider as their cb function
  start_urls = ['http://www.livingsocial.com/cities/15-san-francisco'] 

  # if a <ul class= is defined as “unstyled cities-items”, 
  # then go within that <ul> element to find <li> elements that 
  # have a parameter called dealid
  deals_list_xpath = '//li[@dealid]'
  item_fields = {
    'title': './/span[@itemscope]/meta[@itemprop="name"]/@content',
    'link': './/a/@href',
    'location': './/a/div[@class="deal-details"]/p[@class="location"]/text()',
    'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
    'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
    'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'
  }

  def parse(self, response):
    """
    Default CB used by Scrapy to process download responses

    Testing Contracts:
    @url htpp://www.livingsocial.com/cities/15-san-francisco
    @returns items 1
    @scrapes title link
    """
    
    #get response after making request to some site (data passed to our cb)
    selector = HtmlXPathSelector(response)

    #iterate over deals
    #selector.select lets us grab the data we defined in deals_lsit_xpath and item_field
    #iterate because will be multiple deals on a single page
    for deal in selector.select(self.deals_list_xpath):
      #load the deals so can process the data into LivingSocialDeal
      loader = XPathItemLoader(LivingSocialDeal(), selector=deal)

      #define processors
        #strip out whitespace of unicode strings
        #join the data together
      loader.default_input_processor = MapCompose(unicode.strip)
      loader.default_input_processor = Join() #no seperator so data joined by a space

      #iterate over fields and add xpaths to the loader
      for field, xpath in self.item_fields.iteritems():
        #add specific data pieces xpath to the loader
        loader.add_xpath(field, xpath)
      #process each data parcel. Grabs title, link, location etc for each deal
        #and get its xpath, process its data with input/output processor
      #yield each item then move onto next deal we find
      yield loader.load_item()
      #First time our function runs it will run from beginning till hits yield
      #Then returns the first value of our loop
      #Then each other call will run the loopi n our function one more time
      # till no value left to return
      #generator is 'empty' once the func runs but doesn't hit yeild anymore
        #this can be because loop has come to an end or if/else fails

