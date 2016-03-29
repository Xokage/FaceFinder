import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from FaceFinder.items import TwitterItem
from brpy import init_brpy
import os
import errno
import urllib2

class TwitterSpider(scrapy.Spider):
    name       = "twitterspider"
    allowed_domains = ["mobile.twitter.com"]
    start_urls  = ["https://mobile.twitter.com/Cristiano"]
    br = init_brpy(br_loc='/usr/local/lib') #Default openbr lib location.
    comparision_list = []
    pass_score = 1   
    
    #initialize spider
    def start_requests(self):
        #OpenBR init
        self.br.br_initialize_default()
        self.br.br_set_property('algorithm','FaceRecognition') #Algorithm to compare faces
        self.br.br_set_property('enrollAll','false')   #Only 1 face per image (if enrollAll true then get all faces from images)
        #Be sure directories exists
        try:
            os.makedirs('gallery')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        try:
            os.makedirs('downloads')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        try:
            os.makedirs('downloads/images')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        #Add images to br
        files = []
        directories = ["gallery"]                    
        while(directories): #Repeat until no more subdirectories found
            for root, dirs, files in os.walk(directories[0], topdown=False):
                for name in files:
                    image = open(os.path.join(root, name)).read()
                    tmpl = self.br.br_load_img(image, len(image))
                    query = self.br.br_enroll_template(tmpl) #append to class list of templates
                    nquery = self.br.br_enroll_template(tmpl)
                    self.comparision_list.append((query,nquery))
                for name in dirs:
                    print(os.path.join(root, name))
            directories.pop(0)
            directories.extend(dirs)
            dirs = []

        return [scrapy.Request(self.start_urls[0])]

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
        for image in response.xpath("//img[contains(@src,'pbs.twimg.com/media')]"):
            #Get image and compare it
            imageurl = str(image.xpath('@src').extract())[3:-2]
            image_to_compare = self.get_image(imageurl)

            # load and enroll image from URL
            image = open(image_to_compare).read()
            tmpl = self.br.br_load_img(image, len(image))
            targets = self.br.br_enroll_template(tmpl)
            ntargets = self.br.br_num_templates(targets)

            # compare and collect scores
            for query, nquery in self.comparision_list:
                scoresmat = self.br.br_compare_template_lists(targets, query)
                for r in range(ntargets):
                    for c in range(nquery):
                        scores.append((imurl, br.br_get_matrix_output_at(scoresmat, r, c)))

            # clean up - no memory leaks
                self.br.br_free_template(tmpl)
                self.br.br_free_template_list(targets)
            
            #get max score
            maxscore = 0
            for score in scores:
                if score > maxscore:
                    maxscore = score
            #compare with pass score
            if maxscore >= pass_score:
                item = TwitterItem()
                item['account']  = account
                item['imageUrl'] = imageurl
                item['tweetUrl'] = response.url
                item['occurrence'] = maxscore         
                yield item

    #def check_occurrence(self, image):

    def get_image(self, url):
        attempts = 0
        filename = str(url[28:url.find('.jpg')])
        if (not os.path.isfile("downloads/images/" + filename + '.jpg')):
            while attempts < 3:
                try:
                    response = urllib2.urlopen(url, timeout = 5)
                    content = response.read()

                    print filename
                    f = open( "downloads/images/" + filename + '.jpg', 'w' )
                    print filename
                    f.write( content )
                    f.close()
                    break
                except urllib2.URLError as e:
                    attempts += 1
                    print type(e)
        else:
            print "Already downloaded!"

        return "downloads/images/" + filename + '.jpg'
