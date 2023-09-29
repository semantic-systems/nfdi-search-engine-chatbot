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
from langchain.llms.base import LLM

class NFDIChatModel:
    dataset_name: str = main_config["DATASET"]
    retriever_name: str = main_config["RETRIEVER"]
    llm_name: str = main_config["LLM"]

    retriever: Retriever = eval(retriever_config[retriever_name])(
        document_processor=eval(dataset_config[dataset_name]["document_processor"])()
    )
    llm: LLM = eval(llm_config[llm_name]["MODEL"])()

    chatbot_chain = None

    def set(self, docs: Any):
        retriever_db = self.retriever.build_retriever(docs=docs)
        self.chatbot_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever_db,
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )
        )

    def chat(self, question: str):
        result = self.chatbot_chain({"question": question})
        return result["answer"]

    def reset(self, docs: Any):
        self.set(docs)
