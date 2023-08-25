# -*- coding: utf-8 -*-
from typing import Any, Dict

from nfdichat.common.config import dataset_config
from nfdichat.common.util import io


class Dataset:
    def __int__(self):
        pass

    def fetch(self) -> [str, Dict]:
        pass


class DocumentProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process(items: Any):
        pass


class ToyDataset(Dataset):
    def __init__(self):
        pass

    def fetch(self) -> [str, Dict]:
        toy_data = io.read_json(dataset_config["toy"]["path"])
        search_query = toy_data["Search Term"]
        retrieved_items = toy_data["results"]
        return search_query, retrieved_items


class ToyDatasetDocumentProcessor(DocumentProcessor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def process(items):
        processed_docs = []
        for parent_key, docs in items.items():
            for doc in docs:
                processed_doc = f"{parent_key.lower()}: "
                for chield_key, info in doc.items():
                    if info == "":
                        continue
                    processed_doc += f"{chield_key} is '{info}', "
                processed_docs.append(processed_doc)
        return processed_docs
