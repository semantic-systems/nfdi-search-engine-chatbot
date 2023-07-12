# -*- coding: utf-8 -*-
"""
Configuration package that provides a set of different configs and default parameters.
"""
from pathlib import Path


class CrawlerConfig:
    """
    Search engine crawler configs to build toy search engine samples
    """

    QUERY_TEMPLATE = (
        "https://nfdi-search.nliwod.org/sources?txtSearchTerm={search_term}"
    )
    TOY_SE_SAMPLES_ROOT_DIR = (
        Path(__file__).parents[3].__str__() + "/assets/toy-se-samples"
    )
