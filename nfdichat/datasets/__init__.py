# -*- coding: utf-8 -*-
""" Package for the dataset component. """
from nfdichat.datasets.dataset import (Dataset, DocumentProcessor,
                                       NFDISearchDataset,
                                       NFDISearchDocumentProcessor,
                                       NFDISearchResultsDocumentProcessor,
                                       ToyDataset, ToyDatasetDocumentProcessor)

__all__ = [
    "Dataset",
    "DocumentProcessor",
    "ToyDataset",
    "ToyDatasetDocumentProcessor",
    "NFDISearchDataset",
    "NFDISearchDocumentProcessor",
    "NFDISearchResultsDocumentProcessor",
]
