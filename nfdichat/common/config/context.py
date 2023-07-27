# -*- coding: utf-8 -*-
"""
Configuration package that provides a set of different configs and default parameters.
Provides a set of global variables.
"""
from pathlib import Path

from nfdichat.common.util.data_structure import StrictDict

dataset_config = StrictDict(
    {
        "TOY_DATASEt_PATH": Path(__file__).parents[3].__str__()
        + "/assets/toy-data/query-1.json"
    }
)
