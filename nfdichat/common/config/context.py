# -*- coding: utf-8 -*-
"""
Configuration package that provides a set of different configs and default parameters.
Provides a set of global variables.
"""
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from nfdichat.common.util.data_structure import StrictDict

_ = load_dotenv(find_dotenv())

main_config = StrictDict(
    {
        "DATASET": os.environ["DATASET"],
        "RETRIEVER": os.environ["RETRIEVER"],
        "LLM": os.environ["LLM"],
        "SEARCH_RESULTS_DIR": os.environ["SEARCH_RESULTS_DIR"],
        "SEARCH_RESULTS_RAW_FILE_NAME": os.environ["SEARCH_RESULTS_RAW_FILE_NAME"],
        "SEARCH_RESULTS_PROCESSED_FILE_NAME": os.environ[
            "SEARCH_RESULTS_PROCESSED_FILE_NAME"
        ],
        "SEARCH_RESULTS_EMBEDDINGS_FILE_NAME": os.environ[
            "SEARCH_RESULTS_EMBEDDINGS_FILE_NAME"
        ],
        "CHAT_HISTORY_FILE_NAME": os.environ["CHAT_HISTORY_FILE_NAME"],
    }
)

dataset_config = StrictDict(
    {
        "toy": {
            "path": f"{Path(__file__).parents[3].__str__()}/assets/toy-data/query-1.json",
            "dataset": "ToyDataset",
            "document_processor": "ToyDatasetDocumentProcessor",
        },
        "nfdi-search": {
            "dataset": "NFDISearchDataset",
            "document_processor": "NFDISearchResultsDocumentProcessor",
        },
    }
)

retriever_config = StrictDict(
    {
        # "RETRIEVER_LM_HUGGINGFACE_REPO": ("allenai/specter2_base"),
        # "RETRIEVER_LM_HUGGINGFACE_REPO": ("allenai/specter2"),
        "RETRIEVER_LM_HUGGINGFACE_REPO": ("sentence-transformers/all-MiniLM-L6-v2"),
        "K": 10,
        "DEVICE": "cpu",
        "tfidf": "TFIDFBasedRetriever",
        "svm": "SVMBasedRetriever",
        "ensemble": "EnsembleBasedRetriever",
        
    }
)

llm_config = StrictDict(
    {
        "vicuna": {
            "MODEL": "VicunaLLM",
            "KEY": os.environ["VICUNA_KEY"],
            "URL": os.environ["VICUNA_URL"],
            "MODEL_VERSION": os.environ["VICUNA_MODEL_VERSION"],
            "TEMPERATURE": os.environ["VICUNA_TEMPERATURE"],
        },
        "openai": {
            "MODEL": "OpenAILLM",
            "MODEL_VERSION": os.environ["OPENAI_MODEL_VERSION"],
            "KEY": os.environ["OPENAI_API_KEY"],
            "TEMPERATURE": os.environ["OPENAI_TEMPERATURE"],
        },
    }
)
