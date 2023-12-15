# -*- coding: utf-8 -*-
"""
Retriever package that provides a set of different retrievers.
"""
import datetime
from typing import Any

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.retrievers import (EnsembleRetriever, KNNRetriever,
                                  TFIDFRetriever)
from langchain.retrievers.svm import SVMRetriever

from nfdichat.common.config import retriever_config
from nfdichat.datasets import DocumentProcessor


class Retriever:
    config = retriever_config

    def __init__(self, document_processor: DocumentProcessor):
        self.document_processor = document_processor

    def process(self):
        pass

    def load_embedding(self) -> HuggingFaceEmbeddings:
        print(
            f"{datetime.datetime.now()}    Loading Embedding from HuggingFaceEmbeddings"
        )
        embedding = HuggingFaceEmbeddings(
            model_name=self.config["RETRIEVER_LM_HUGGINGFACE_REPO"],
            model_kwargs={"device": self.config["DEVICE"]},
        )
        return embedding

    def build_retriever(self, docs: Any) -> Any:
        pass


class SVMBasedRetriever(Retriever):
    def __init__(self, document_processor: DocumentProcessor, **kwargs):
        super().__init__(document_processor)
        self.embedding = self.load_embedding()

    def build_retriever(self, docs: Any) -> Any:
        processed_docs = self.document_processor.process(items=docs)
        retriever_db = SVMRetriever.from_texts(
            embeddings=self.embedding, texts=processed_docs, k=self.config["K"]
        )
        return retriever_db


class EnsembleBasedRetriever(Retriever):
    def __init__(self, document_processor: DocumentProcessor, **kwargs):
        super().__init__(document_processor)
        self.embedding = self.load_embedding()

    def build_retriever(self, docs: Any) -> Any:
        processed_docs = self.document_processor.process(items=docs)
        tfidf_retriever = TFIDFRetriever.from_texts(
            texts=processed_docs, k=self.config["K"]
        )
        knn_retriever = KNNRetriever.from_texts(
            texts=processed_docs, embeddings=self.embedding, k=self.config["K"]
        )
        retriever_db = EnsembleRetriever(
            retrievers=[tfidf_retriever, knn_retriever], weights=[0.4, 0.6]
        )
        return retriever_db


class TFIDFBasedRetriever(Retriever):
    def __init__(self, document_processor: DocumentProcessor, **kwargs):
        super().__init__(document_processor)

    def build_retriever(self, docs: Any) -> Any:
        processed_docs = self.document_processor.process(items=docs)
        retriever_db = TFIDFRetriever.from_texts(
            texts=processed_docs, k=self.config["K"]
        )
        return retriever_db
