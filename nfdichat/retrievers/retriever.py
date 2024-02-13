# -*- coding: utf-8 -*-
"""
Retriever package that provides a set of different retrievers.
"""
import datetime
import os
from typing import Any

import numpy as np
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.retrievers import (EnsembleRetriever, KNNRetriever,
                                  TFIDFRetriever)
from langchain.retrievers.svm import SVMRetriever

from nfdichat.common.config import main_config, retriever_config
from nfdichat.common.util import io
from nfdichat.datasets import DocumentProcessor


class Retriever:
    main_config = main_config
    config = retriever_config

    def __init__(self, document_processor: DocumentProcessor):
        self.document_processor = document_processor

    def process(self):
        pass

    def load_embedding(self) -> HuggingFaceEmbeddings:
        print(
            f"{datetime.datetime.now()} - Loading Embedding from HuggingFaceEmbeddings"
        )
        embedding = HuggingFaceEmbeddings(
            model_name=self.config["RETRIEVER_LM_HUGGINGFACE_REPO"],
            model_kwargs={"device": self.config["DEVICE"]},
            # multi_process=True,
        )
        return embedding

    def save_docs_with_embeddings(self, docs: Any, uuid: str) -> Any:
        directory_path = os.path.join(self.main_config["SEARCH_RESULTS_DIR"], uuid)
        io.create_dir(directory_path)

        search_results_file_path = os.path.join(
            directory_path, self.main_config["SEARCH_RESULTS_RAW_FILE_NAME"]
        )
        search_results_processed_file_path = os.path.join(
            directory_path, self.main_config["SEARCH_RESULTS_PROCESSED_FILE_NAME"]
        )
        search_results_embeddings_file_path = os.path.join(
            directory_path, self.main_config["SEARCH_RESULTS_EMBEDDINGS_FILE_NAME"]
        )
        chat_history_file_path = os.path.join(
            directory_path, main_config["CHAT_HISTORY_FILE_NAME"]
        )

        # save the raw search results to a json file
        io.write_json(search_results_file_path, docs)
        # process the search results
        processed_docs = self.document_processor.process(items=docs)
        # save the processed search results to a json file
        io.write_json(search_results_processed_file_path, processed_docs)

        # now generate the embeddings for all the search results
        self.embedding = self.load_embedding()
        # result = []
        # for doc in processed_docs:
        #     result.append(self.embedding.embed_query(doc))
        result = self.embedding.embed_documents(processed_docs)
        io.write_numpy_array(search_results_embeddings_file_path, np.array(result))

        # save the empty chat history to the file
        chat_history_list = []
        io.write_json(chat_history_file_path, chat_history_list)

        return np.array(result)

    def build_retriever(self, docs: Any) -> Any:
        pass


class SVMBasedRetriever(Retriever):
    def __init__(self, document_processor: DocumentProcessor, **kwargs):
        super().__init__(document_processor)
        self.embedding = self.load_embedding()

    def build_retriever(self, search_uuid: str) -> Any:
        # processed_docs = self.document_processor.process(items=docs)
        directory_path = os.path.join(
            self.main_config["SEARCH_RESULTS_DIR"], search_uuid
        )
        search_results_processed_file_path = os.path.join(
            directory_path, self.main_config["SEARCH_RESULTS_PROCESSED_FILE_NAME"]
        )
        search_results_embeddings_file_path = os.path.join(
            directory_path, self.main_config["SEARCH_RESULTS_EMBEDDINGS_FILE_NAME"]
        )

        processed_docs = io.read_json(search_results_processed_file_path)
        index = io.read_numpy_array(search_results_embeddings_file_path)
        retriever_db = SVMRetriever(
            index=index,
            texts=processed_docs,
            embeddings=self.embedding,
            k=self.config["K"],
        )
        # retriever_db = SVMRetriever.from_texts(
        #     embeddings=self.embedding, texts=processed_docs, k=self.config["K"]
        # )
        return retriever_db

class TFIDFBasedRetriever(Retriever):
    def __init__(self, document_processor: DocumentProcessor, **kwargs):
        super().__init__(document_processor)

    def build_retriever(self, search_uuid: str) -> Any:
        directory_path = os.path.join(
            self.main_config["SEARCH_RESULTS_DIR"], search_uuid
        )
        search_results_processed_file_path = os.path.join(
            directory_path, self.main_config["SEARCH_RESULTS_PROCESSED_FILE_NAME"]
        )
        processed_docs = io.read_json(search_results_processed_file_path)        
        retriever_db = TFIDFRetriever.from_texts(
            texts=processed_docs, k=self.config["K"]
        )
        return retriever_db
    
class EnsembleBasedRetriever(Retriever):
    def __init__(self, document_processor: DocumentProcessor, **kwargs):
        super().__init__(document_processor)
        self.embedding = self.load_embedding()

    def build_retriever(self, search_uuid: str) -> Any:
        directory_path = os.path.join(
            self.main_config["SEARCH_RESULTS_DIR"], search_uuid
        )
        search_results_processed_file_path = os.path.join(
            directory_path, self.main_config["SEARCH_RESULTS_PROCESSED_FILE_NAME"]
        )
        processed_docs = io.read_json(search_results_processed_file_path)

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



