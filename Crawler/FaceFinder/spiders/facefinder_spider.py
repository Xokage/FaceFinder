import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from FaceFinder.items import TwitterItem

class TwitterSpider(scrapy.Spider):
    name       = "twitterspider"
    allowed_domains = ["mobile.twitter.com"]
    start_urls  = ["https://mobile.twitter.com/Cristiano"]
#    rules = (
#    Rule(LinkExtractor(restrict_xpaths=("//a[contains(@class,'twitter-atreply dir-ltr')]/@href")), follow=True),
#    Rule(LinkExtractor(restrict_xpaths=("//div[@class='w-button-more']/a/@href")), follow=True),
#    )

    #Get what tweets has images
    def parse(self, response):
        for tweet in response.xpath("//table[contains(@class,'tweet')]"):
            #check if it has a picture in tweet
            if tweet.xpath("//a[contains(@class, 'twitter_external_link dir-ltr tco-link has-expanded-path')]") is not None:
                url = response.urljoin(str(tweet.xpath("@href").extract())[4:-6])
                yield scrapy.Request(url, callback=self.parse_image)
            #check if it mentions someone
        for mention in response.xpath("//a[contains(@class,'twitter-atreply dir-ltr')]"):
            url = response.urljoin(str(mention.xpath("@href").extract())[4:-2])
            yield scrapy.Request(url)
        url = response.urljoin(str(response.xpath("//div[@class='w-button-more']/a/@href").extract())[4:-2])
        print url
        if url is not None:
            yield scrapy.Request(url)


    #Fetch all images posted.
    def parse_image(self, response):
        account = ''
        if '/status/' in response.url:
             account = response.url[27:response.url.find('/status')]
        print 'Url: ' + response.url
        for image in response.xpath("//img[contains(@src,'pbs.twimg.com/media')]"):
            item = TwitterItem()
            item['account']  = account
            item['imageUrl'] = str(image.xpath('@src').extract())[3:-2]
            item['tweetUrl'] = response.url          
            yield item
