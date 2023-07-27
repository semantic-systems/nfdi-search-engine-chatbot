# -*- coding: utf-8 -*-
"""
Configuration package that provides a set of different configs and default parameters.
"""
from pathlib import Path


class DatasetConfig:
    """
    Search engine dataset configs to build engine samples
    """

    TOY_DATASET_PATH = (
        Path(__file__).parents[3].__str__() + "/assets/toy-data/query-1.json"
    )
