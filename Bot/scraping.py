# This script provides a reusable module for web scraping Telegram channels from the telemetr.io website

from multiprocessing import Process
from multiprocessing import Queue
from scrapy import Spider
from scrapy import Request
from scrapy.crawler import CrawlerProcess


channels = []  # List of channels to store results during the scraping process
query = None  # Search query value during the parsing process


class ChannelSpider(Spider):
    name = 'channels'

    def start_requests(self):
        # Generating URLs for web scraping based on search query and page number
        for i in range(1, 11):
            if query:
                page = f'https://telemetr.io/en/channels?channel={query}&page={i}'
            else:
                page = f'https://telemetr.io/en/channels?page={i}'
            yield Request(url=page, callback=self.parse)

    def parse(self, response):
        # Extracting channel data from response and adding them to list of scraped channels
        for channel_block in response.css('div.info-channel'):
            username = channel_block.css('div.username-block *::text').get()
            name = channel_block.css('div.name-block *::text').get()
            if username[0] == '@':
                channel = {'name': name, 'username': username}
                channels.append(channel)


process = CrawlerProcess()  # Process to run the Scrapy crawler
crawler = process.create_crawler(ChannelSpider)  # Instance of the Scrapy crawler


def crawl(search_query=None, result_queue=None):
    # Reset the channel list and update the search query for the new parsing process
    global channels
    channels = []
    global query
    query = search_query

    # Start the web scraping process by running the crawler
    process.crawl(crawler)
    process.start()
    process.stop()

    # Removing duplicate channels
    unique_channels = []
    for channel in channels:
        if channel not in unique_channels:
            unique_channels.append(channel)

    # Putting the channel list in the result queue
    result_queue.put(unique_channels)


def search(search_query=None):
    """
    Function that returns a list of channels for a given search query
    """
    # Queue to store the result of the process
    result_queue = Queue()

    # Starting the crawler process and waiting for it to finish
    crawler_process = Process(target=crawl, args=(search_query, result_queue))
    crawler_process.start()
    crawler_process.join()

    # Getting a list of channels from the result queue
    channels = result_queue.get()

    return channels
