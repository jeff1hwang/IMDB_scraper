# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt9376612/']

    def parse(self, response):
        '''
        This method tells the spider what to do 
        when we get to the website
        '''
        # response is how scrapy stores the website
        cast_crew_url = response.url + "fullcredits/"

        # navigating to the case and crew page
        # using scrapy.Request() method
        # then, navigate to the next link and parse_full_credits()
        # will be call
        yield scrapy.Request(cast_crew_url, callback=self.parse_full_credits)
    
    def parse_full_credits(self, response):
        '''
        This function parse the series cast page for the movie,
        and it will then navigate to each actor's page
        '''
        # collect a list of actors links
        cast_link = [actors.attrib["href"] for actors in response.css("td.primary_photo a")]

        # iterate over each actor's link
        # then yield the request to the next function
        for link in cast_link:
            url = "https://www.imdb.com" + link
            
            yield scrapy.Request(url, callback = self.parse_actor_page)

    
    def parse_actor_page(self, response):
        actor_name = response.css("span.itemprop::text").get()

        movie_list = response.css("div.filmo-row b a::text").getall()

        for movie in movie_list:
            yield {
                "actor" : actor_name,
                "Movie_or_TV_name" : movie
            }
