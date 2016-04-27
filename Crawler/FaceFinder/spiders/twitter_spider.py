import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from FaceFinder.items import TwitterItem
from brpy import init_brpy
import os
import errno
import urllib2
import logging
class TwitterSpider(scrapy.Spider):
    ''' Lista argumentos:
        start_url,
        image_dir,
        downloads_dir.
    '''

    name       = "twitterspider"
    allowed_domains = ["mobile.twitter.com"]
    start_url = ""
    br = init_brpy(br_loc='/usr/local/lib') #Default openbr lib location.
    comparision_list = []
    tmpl_list = []
    pass_score = 0.1
    image_dir = "default"
    downloads_dir = "default"
    person_id = 0
    #Override init so it can be called with arguments
    def __init__(self, *args, **kwargs):
        super(TwitterSpider, self).__init__(*args, **kwargs)
        url = kwargs.get('start_url', '')
        if(url != ''):
            self.start_url = url
        image_dir = kwargs.get('image_dir','')
        if(image_dir != ''):
            self.image_dir = image_dir
        downloads_dir = kwargs.get('downloads_dir','')
        if(downloads_dir != ''):
            self.downloads_dir = downloads_dir
        try:
            person_id = int(float(kwargs.get('person_id','')))
            if(person_id > 0):
                self.person_id = person_id
        except ValueError:
            self.person_id = 0
    #initialize spider
    def start_requests(self):
        #OpenBR init
        logging.debug("Initializating openbr!")
        self.br.br_initialize_default()
        self.br.br_set_property('algorithm','FaceRecognition') #Algorithm to compare faces
        self.br.br_set_property('enrollAll','false')   #Only 1 face per image (if enrollAll true then get all faces from images)
        #Be sure directories exists
        try:
            os.makedirs(self.image_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        try:
            os.makedirs(self.downloads_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        #Add images to br
        files = []
        directories = [self.image_dir]                    
        logging.debug("Loading images from %s." % self.image_dir)
        count = 0
        while(directories): #Repeat until no more subdirectories found
            for root, dirs, files in os.walk(directories[0], topdown=False):
                for name in files:
                    image = open(os.path.join(root, name)).read()
                    tmpl = self.br.br_load_img(image, len(image))
                    self.tmpl_list.append(tmpl)
                    query = self.br.br_enroll_template(tmpl) #append to class list of templates
                    nquery = self.br.br_num_templates(tmpl)
                    self.comparision_list.append((query,nquery))
                    count = count + 1
            directories.pop(0)
            directories.extend(dirs)
            dirs = []
        logging.debug("Loaded {0} images.".format(count))
        if(self.start_url is None or self.start_url == ''):
            return ""
        else:
            return [scrapy.Request(self.start_url)]

    #Get what tweets has images
    def parse(self, response):
        for tweet in response.xpath("//table[contains(@class,'tweet')]"):
            #check if it has a picture in tweet
            if tweet.xpath("//a[contains(@class, 'twitter_external_link dir-ltr tco-link has-expanded-path')]") is not None:
                url = response.urljoin(str(tweet.xpath("@href").extract())[4:-6])
                yield scrapy.Request(url, callback=self.parse_image)
        #check if it mentions someone only if it's one of the start urls (so it wont keep crawling indefinitely)
        url = response.urljoin(str(response.xpath("//div[@class='w-button-more']/a/@href").extract())[4:-2])
        if url is not None:
            yield scrapy.Request(url)
        if response.url == self.start_url:
            for mention in response.xpath("//a[contains(@class,'twitter-atreply dir-ltr')]"):
                url = response.urljoin(str(mention.xpath("@href").extract())[4:-2])
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

            # compare with all images
            scores = []

            for query, nquery in self.comparision_list:
                scoresmat = self.br.br_compare_template_lists(targets, query)
                for r in range(ntargets):
                    for c in range(nquery):
                        scores.append((imageurl, self.br.br_get_matrix_output_at(scoresmat, r, c)))
            # clean up - no memory leaks
            self.br.br_free_template(tmpl)
            self.br.br_free_template_list(targets)


            # print top 10 match URLs
            scores.sort(key=lambda s: s[1])
            maxscore = float("-inf")
            for url, score in scores:
                if(score > maxscore):
                    maxscore = score
            #compare with pass score
            if maxscore >= self.pass_score:
                item = TwitterItem()
                item['account']  = account
                item['imageUrl'] = imageurl
                item['tweetUrl'] = response.url
                item['occurrence'] = maxscore
                if(self.person_id > 0):
                    item['person_id'] = self.person_id
                yield item

    #def check_occurrence(self, image):

    def get_image(self, url):
        attempts = 0
        filename = str(url[28:url.find('.jpg')])
        if (not os.path.isfile(os.path.join(self.downloads_dir,filename + '.jpg'))):
            while attempts < 3:
                try:
                    response = urllib2.urlopen(url, timeout = 5)
                    content = response.read()
                    f = open(os.path.join(self.downloads_dir, filename + '.jpg'), 'w' )
                    f.write( content )
                    f.close()
                    break
                except urllib2.URLError as e:
                    attempts += 1
                    logging.error(type(e))
        else:
            logging.debug("Already downloaded!")

        return os.path.join(self.downloads_dir,filename + '.jpg')

    def closed(self, reason):
        logging.info("Freeing memory from openbr.")
        for tmpl in self.tmpl_list:
            self.br.br_free_template(tmpl)
        for query, nqueries in self.comparision_list:
            self.br.br_free_template_list(query)
        self.br.br_finalize()
