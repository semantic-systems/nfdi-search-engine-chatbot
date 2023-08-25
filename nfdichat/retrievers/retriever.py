# -*- coding: utf-8 -*-
"""
Retriever package that provides a set of different retrievers.
"""
from typing import Any

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.retrievers.svm import SVMRetriever

from nfdichat.common.config import retriever_config
from nfdichat.datasets import DocumentProcessor


class Retriever:
    config = retriever_config

    def __init__(self, document_processor: DocumentProcessor):
        self.document_processor = document_processor
        self.embedding = self.load_embedding()

    def process(self):
        pass

    def load_embedding(self) -> HuggingFaceEmbeddings:
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

    def build_retriever(self, docs: Any) -> Any:
        processed_docs = self.document_processor.process(items=docs)
        retriever_db = SVMRetriever.from_texts(
            embeddings=self.embedding, texts=processed_docs, k=self.config["K"]
        )
        return retriever_db
