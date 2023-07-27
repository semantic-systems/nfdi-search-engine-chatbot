# -*- coding: utf-8 -*-
"""
A script for creating toy data needed to use the chatbot in demos and testing enviroment.
"""
from nfdichat.common.config.dataset import DatasetConfig
from nfdichat.common.util import io
from nfdichat.dataset.nfdi_dataset import NFDIDataset


class ToyDataset(NFDIDataset):
    def __int__(self):
        super.__init__()
        self.nfdi_search_data = {}
        self.toy_data = io.read_json(DatasetConfig.TOY_DATASET_PATH)
