# -*- coding: utf-8 -*-
"""
Configuration package that provides a set of different configs and default parameters.
"""


class CrawlerConfig:
    """
    Search engine crawler configs to build toy search engine samples
    """

    QUERY_TEMPLATE = "https://nfdi-search.nliwod.org/sources?txtSearchTerm={query_term}"
