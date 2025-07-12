import scrapy


class WebScraper(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://www.unicatt.it/',
    ]

    def parse(self, response):
        for quote in response.css("div.item"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'pretitle': quote.css("h4.pretitle::text").extract_first(),
                'title': quote.css("a.title::text").extract_first(),
            }

