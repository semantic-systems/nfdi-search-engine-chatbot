# -*- coding: utf-8 -*-
"""
A script for creating toy data needed to use the chatbot in demos and testing enviroment.
"""
from nfdichat.common.configs import config


def main():
    conf = config.CrawlerConfig()
    print(conf.QUERY_TEMPLATE)
    print(conf.TOY_SE_SAMPLES_ROOT_DIR)
    print("RUNNING MAIN")


if __name__ == "__main__":
    main()
