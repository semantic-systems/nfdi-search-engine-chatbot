# -*- coding: utf-8 -*-
# """ Package for the dataset component. """
from nfdichat.retrievers.retriever import (EnsembleBasedRetriever, Retriever,
                                           SVMBasedRetriever,
                                           TFIDFBasedRetriever)

__all__ = [
    "SVMBasedRetriever",
    "Retriever",
    "EnsembleBasedRetriever",
    "TFIDFBasedRetriever",
]
