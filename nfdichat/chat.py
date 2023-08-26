# -*- coding: utf-8 -*-
"""
Root script of NFDI Search Engine ChatBot (nfdichat)
"""
from typing import Any

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from nfdichat.common.config import (dataset_config, llm_config, main_config,
                                    retriever_config)
from nfdichat.datasets import (Dataset, DocumentProcessor,
                               ToyDatasetDocumentProcessor)
from nfdichat.llms import VicunaLLM
from nfdichat.retrievers import Retriever, SVMBasedRetriever
from nfdichat.template import CHAIN_PROMPT


class NFDIChatModel:
    dataset_name: str = main_config["DATASET"]
    retriever_name: str = main_config["RETRIEVER"]
    llm_name: str = main_config["LLM"]

    # dataset: Dataset = dataset_config[dataset_name]['dataset']()
    retriever: Retriever = eval(retriever_config[retriever_name])(
        document_processor=eval(dataset_config[dataset_name]["document_processor"])()
    )
    llm = eval(llm_config[llm_name]["MODEL"])()

    # chat_history = []
    chatbot_chain = None

    def set(self, docs: Any):
        retriever_db = self.retriever.build_retriever(docs=docs)
        # cls.chat_history = []
        self.chatbot_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever_db,
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            ),
        )

    def chat(self, question: str):
        result = self.chatbot_chain({"question": question})
        # self.chat_history.extend([(question, result["answer"])])
        return result["answer"]

    def reset(self, docs: Any):
        self.__new__(docs)
