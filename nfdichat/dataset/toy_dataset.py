# -*- coding: utf-8 -*-
"""
A script for creating toy data needed to use the chatbot in demos and testing enviroment.
"""
from nfdichat.common.configs.config import CrawlerConfig
from nfdichat.common.tools import crawler

toy_query_terms = [
    "Ricardo Usbeck",
    "Jennifer D'Souza",
    "Tilahun Abedissa",
    "Hamed Babaei Giglou",
    "fake news",
    "knowledge graph",
    "large language models",
    "open research knowledge graph",
    "nfdi",
    "question answering",
    "Germany",
    "University of Hamburg",
]


class ToyDataset:
    def __init__(self):
        self.nfdi_search_crawled_data = {}
        self.query_template = CrawlerConfig.QUERY_TEMPLATE

    def preprocess_query(self, query_term: str) -> str:
        query_term = query_term.replace(" ", "+")
        return query_term

    def crawl_queries(self) -> None:
        for query_term in toy_query_terms:
            query_term_cleaned = self.preprocess_query(query_term=query_term)
            query_url = self.query_template.replace("{query_term}", query_term_cleaned)
            crawled_data = crawler.crawl(url=query_url)
            self.nfdi_search_crawled_data[query_term] = {
                "query-url": query_url,
                "crawled-data": crawled_data,
            }


if __name__ == "__main__":
    c = ToyDataset()
    c.crawl_queries()
