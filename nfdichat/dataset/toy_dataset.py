# -*- coding: utf-8 -*-
"""
A script for creating toy data needed to use the chatbot in demos and testing enviroment.
"""
from typing import Dict

from nfdichat.common.config.dataset import DatasetConfig
from nfdichat.common.util import io
from nfdichat.dataset.nfdi_dataset import NFDIDataset


class ToyDataset(NFDIDataset):
    def __init__(self):
        pass

    def fetch(self) -> [str, Dict]:
        toy_data = io.read_json(DatasetConfig.TOY_DATASET_PATH)
        search_query = toy_data["Search Term"]
        retrieved_items = toy_data["results"]
        return search_query, retrieved_items
