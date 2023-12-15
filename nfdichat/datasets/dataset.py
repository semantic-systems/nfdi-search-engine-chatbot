# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from nfdichat.common.config import dataset_config
from nfdichat.common.util import io


class Dataset:
    def __int__(self):
        pass

    @staticmethod
    def fetch(self, **kwargs) -> [str, Dict]:
        pass


class DocumentProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process(items: Any):
        pass


class ToyDataset(Dataset):
    def fetch(self, **kwargs) -> [str, Dict]:
        toy_data = io.read_json(dataset_config["toy"]["path"])
        search_query = toy_data["Search Term"]
        retrieved_items = toy_data["results"]
        return search_query, retrieved_items


class ToyDatasetDocumentProcessor(DocumentProcessor):
    def process(self, items):
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


class NFDISearchDataset(Dataset):
    def __init__(self):
        pass

    def fetch(self, **kwargs) -> [str, Dict]:
        data = kwargs["results"][0]
        search_query = data["search_key"]
        retrieved_items = data["results"]
        return search_query, retrieved_items


class NFDISearchDocumentProcessor(DocumentProcessor):
    IN_VALID_KEYS = ["timedout_sources"]
    VALID_DATA_KEYS = [
        "name",
        "author",
        # "description",
        "keywords",
        "source",
        "abstract",
        "license",
        "datePublished",
        "dateModified",
        "dateCreated",
        "inLanguage",
        "publisher",
        "orcid",
        "affiliation",
        "address",
        "text",
    ]
    VALID_DATA_KEY_LIST_DT = ["inLanguage", "author", "keywords"]
    # list: inLanguage, author, keywords

    def process_single_doc(
        self, parent_topic: str, input_doc: Dict, index: int
    ) -> List:
        processed_doc = []
        for valid_key in self.VALID_DATA_KEYS:
            processed_doc_text = f"{parent_topic.lower()} {str(index + 1)}: \n"
            value = input_doc.get(valid_key, "NONE")
            if str(value).lower() != "none" and value != "":
                if valid_key == "author":
                    new_value = ""
                    for author in value:
                        new_value += (
                            f"{author.get('name')} ({author.get('affiliation', '')}) ,"
                        )

                    value = new_value
                if valid_key == "inLanguage" or valid_key == "keywords":
                    value = ", ".join(value)
                processed_doc_text += (
                    f"- {valid_key[0].upper()+valid_key[1:]} : {value}"
                )
                processed_doc.append(processed_doc_text)
        return processed_doc

    def process(self, items):
        processed_docs = []
        for parent_key, docs in items.items():
            if parent_key not in self.IN_VALID_KEYS:
                for index, doc in enumerate(docs):
                    processed_doc_list = self.process_single_doc(
                        parent_topic=parent_key, input_doc=doc, index=index
                    )
                    for processed_doc in processed_doc_list:
                        processed_docs.append(processed_doc)
        print(
            f":::::::::::::::::::: Processed documents (NO:{len(processed_docs)}) ::::::::::::::"
        )
        return processed_docs
