# healthline_spider.py

import scrapy
from scrapy_playwright.page import PageCoroutine

class HealthlineSpider(scrapy.Spider):
    name = 'healthline'
    allowed_domains = ['healthline.com']
    start_urls = ['https://www.healthline.com/health/autism/what-to-do-autism-meltdown#What-to-do-during-a-very-loud,-very-public-meltdown']

    async def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(url=url))

    async def parse(self, response, url):
        # Use Playwright to interact with the page
        page = await PageCoroutine.from_response(response)

        # Wait for the content to be loaded
        await page.wait_for_selector('.css-axufdj.evys1bk0 article')

        # Extract the entire article content
        title = await page.text('h1')
        content = await page.inner_html('.css-axufdj.evys1bk0 article')

        yield {
            'url': url,
            'title': title,
            'content': content,
        }

        # Close the browser page
        await page.close()


