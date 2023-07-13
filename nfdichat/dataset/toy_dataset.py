# -*- coding: utf-8 -*-
"""
A script for creating toy data needed to use the chatbot in demos and testing enviroment.
"""
from nfdichat.common.configs import CrawlerConfig

toy_queries = [
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
]


def main():
    conf = CrawlerConfig()
    print(conf.QUERY_TEMPLATE)
    print(conf.TOY_SE_SAMPLES_ROOT_DIR)
    print("RUNNING MAIN")


if __name__ == "__main__":
    main()
