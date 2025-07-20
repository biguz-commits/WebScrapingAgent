# scrapy runspider quotes_spider.py

from typing import Tuple

import scrapy
from dotenv import load_dotenv

from app.agent.Embeddings import Embeddings
from app.db.DbConnection import DbConnection
from app.db.services.UnicattService import UnicattService


load_dotenv()


class WebScraper(scrapy.Spider):
    name = "unicatt-latest-news"
    start_urls = [
        'https://www.unicatt.it/',
    ]

    def __init__(self):
        self.embeddings = Embeddings()

    def parse(self, response):
        """Parses and stores the scraped data in memory."""
        parsed_data = []

        for quote in response.css("div.item"):
            current_text = quote.css("span.text::text").extract_first()
            current_pretitle = quote.css("h4.pretitle::text").extract_first()
            current_title = quote.css("a.title::text").extract_first()

            if current_title:
                parsed_data.append({
                    "title": current_title,
                    "pretitle": current_pretitle,
                    "text": current_text
                })

        self._db_update(parsed_data)
        return parsed_data

    def _db_update(self, scraped_items: list[dict]):
        """Updates the database: creates new records or updates existing ones."""
        db, service = self.__get_db_and_service()

        for item in scraped_items:
            item["embedding"] = self.embeddings.vectorialize(item["text"])
            existing = db.query(service.model).filter_by(title=item["title"]).first()

            if existing:
                updated = service.update(db, id=existing.id, **item)
                self.logger.info(f"Updated: {updated.title}")
            else:
                created = service.create(db, **item)
                self.logger.info(f"Inserted: {created.title}")

        db.close()

    @staticmethod
    def  __get_db_and_service() -> Tuple:
        db = DbConnection()
        db_session = db.create_session()
        service = UnicattService()
        return db_session, service


