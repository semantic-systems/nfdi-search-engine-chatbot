# -*- coding: utf-8 -*-
import traceback

from flask import Flask, jsonify, request
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate

from nfdichat.common.config import (dataset_config, llm_config, main_config,
                                    retriever_config)
from nfdichat.datasets import *
from nfdichat.llms import *
from nfdichat.retrievers import *

app = Flask(__name__)

RETRIEVER: Retriever = eval(retriever_config[main_config["RETRIEVER"]])(
    document_processor=eval(
        dataset_config[main_config["DATASET"]]["document_processor"]
    )()
)
LLM_MODEL: LLM = eval(llm_config[main_config["LLM"]]["MODEL"])()


@app.route("/ping")
def ping():
    return "This is NFID-Search ChatBot"


@app.route("/chat", methods=["POST", "GET"])
def chat():
    try:
        # data = request.get_json(force=True)
        # question = data.get("question")
        # chat_history_list = data.get("chat-history")
        # search_results = data.get("search-results")

        import json

        def load_search_results(file_name):
            with open(file_name, "r", encoding="utf8") as f:
                data = json.load(f)
            return data

        data = {}
        # question = "You are talking about who?"
        # question = "What is the latest publication?"
        question = "Who is Ricardo?"
        # question = "What is the title of Ricardo's first publication?"
        chat_history_list = []
        search_results = load_search_results("assets/nfdi-search/results3.json")

        query, items = NFDISearchDataset().fetch(**{"results": search_results})
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        for chat_history in chat_history_list:
            memory.save_context(
                {"input": chat_history["input"]}, {"output": chat_history["output"]}
            )

        # custom_template = """You work for CompanyX which sells things located in United States.
        # If you don't know the answer, just say that you don't. Don't try to make up an answer.
        # Base your questions only on the knowledge provided here. Do not use any outside knowledge.
        # Given the following chat history and a follow up question,
        # rephrase the follow up question to be a standalone question, in its original language.
        # Chat History:
        # {chat_history}
        # Follow Up Input: {question}
        # Standalone question:
        # """
        # CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)
        # CUSTOM_PROMPT = PromptTemplate(
        #     template=prompt_template, input_variables=["context", "question"]
        # )

        custom_template = """Provide your answers only on the knowledge provided here. Do not use any outside knowledge.
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        Given the following context, answer the below question:

        {context}

        Question: {question}
        Helpful Answer:"""
        # CUSTOM_PROMPT = PromptTemplate.from_template(custom_template)
        CUSTOM_PROMPT = PromptTemplate(
            template=custom_template, input_variables=["context", "question"]
        )

        global LLM_MODEL, RETRIEVER
        CHATBOT = ConversationalRetrievalChain.from_llm(
            llm=LLM_MODEL,
            chain_type="stuff",
            retriever=RETRIEVER.build_retriever(docs=items),
            memory=memory,
            # condense_question_prompt=CUSTOM_PROMPT,
            combine_docs_chain_kwargs={"prompt": CUSTOM_PROMPT},
        )
        answer = CHATBOT({"question": question})
        answer = answer["answer"]
        chat_history_list.append({"input": question, "output": answer})
        data["chat-history"] = chat_history_list
        return jsonify(data)

    except Exception as ex:
        data["exception"] = str(ex)
        data["traceback"] = traceback.format_exc()
        print(data["traceback"])
        return jsonify(data)


# @app.route("/generate_embeddings", methods=["POST", "GET"])
# def generate_embeddings():
#     search_results = request.form["search-results"]


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5005")
