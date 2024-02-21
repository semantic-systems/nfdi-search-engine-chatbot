# -*- coding: utf-8 -*-
import datetime
import json
import os
import traceback

from flask import Flask, jsonify, request
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate

from nfdichat.common.config import (dataset_config, llm_config, main_config,
                                    retriever_config)
from nfdichat.common.util import io
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
    return "This is NFDI-Search Chatbot"


@app.route("/chat", methods=["POST", "GET"])
def chat():
    try:
        data = request.get_json(force=True)
        question = data.get("question")
        search_uuid = data.get("search_uuid")

        directory_path = os.path.join(main_config["SEARCH_RESULTS_DIR"], search_uuid)
        chat_history_file_path = os.path.join(
            directory_path, main_config["CHAT_HISTORY_FILE_NAME"]
        )
        chat_history_list = io.read_json(chat_history_file_path)

        data = {}
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        for chat_history in chat_history_list:
            memory.save_context(
                {"input": chat_history["input"]}, {"output": chat_history["output"]}
            )

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
            retriever=RETRIEVER.build_retriever(search_uuid=search_uuid),
            memory=memory,
            # condense_question_prompt=CUSTOM_PROMPT,
            combine_docs_chain_kwargs={"prompt": CUSTOM_PROMPT},
        )
        answer = CHATBOT({"question": question})
        answer = answer["answer"]
        chat_history_list.append({"input": question, "output": answer})

        # update chat history file
        io.write_json(chat_history_file_path, chat_history_list)

        data["chat-history"] = chat_history_list
        return jsonify(data)

    except Exception as ex:
        data["exception"] = str(ex)
        data["traceback"] = traceback.format_exc()
        print(data["traceback"])
        return jsonify(data)


@app.route("/save-docs-with-embeddings/<uuid>", methods=["POST", "GET"])
def save_docs_with_embeddings(uuid):
    search_results = request.get_json()
    search_uuid = uuid
    print("uuid:", search_uuid)

    global RETRIEVER
    RETRIEVER.save_docs_with_embeddings(json.loads(search_results), search_uuid)

    return "success"


@app.route("/are-embeddings-generated/<uuid>", methods=["GET"])
def are_embeddings_generated(uuid):
    response= {}
    print(f"{datetime.datetime.now()} - uuid: {uuid}")
    directory_path = os.path.join(main_config["SEARCH_RESULTS_DIR"], uuid)
    search_results_embeddings_file_path = os.path.join(
            directory_path, main_config["SEARCH_RESULTS_EMBEDDINGS_FILE_NAME"]
        )
    file_exists = io.file_exists(search_results_embeddings_file_path)
    response['file_exists'] = file_exists
    print(f"{datetime.datetime.now()} - response: {response}")
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="6003")
