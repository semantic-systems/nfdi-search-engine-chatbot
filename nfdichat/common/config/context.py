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
    }
)

dataset_config = StrictDict(
    {
        "toy": {
            "path": Path(__file__).parents[3].__str__()
            + "/assets/toy-data/query-1.json",
            "dataset": "ToyDataset",
            "document_processor": "ToyDatasetDocumentProcessor",
        },
    }
)

retriever_config = StrictDict(
    {
        "RETRIEVER_LM_HUGGINGFACE_REPO": ("allenai/specter2_base"),
        "K": 5,
        "DEVICE": "cpu",
        "svm": "SVMBasedRetriever",
    }
)

llm_config = StrictDict(
    {
        "vicuna": {
            "MODEL": "VicunaLLM",
            "KEY": os.environ["VICUNA_KEY"],
            "URL": os.environ["VICUNA_URL"],
            "MODEL_VERSION": os.environ["VICUNA_MODEL_VERSION"],
            "TEMPERATURE": os.environ["TEMPERATURE"],
        }
    }
)
