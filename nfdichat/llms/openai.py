# -*- coding: utf-8 -*-
from typing import Any, Mapping

import requests
from langchain.llms.base import LLM
from openai import OpenAI

from nfdichat.common.config import llm_config
from nfdichat.common.util import helper_functions


class OpenAILLM(LLM):
    config = llm_config["openai"]

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, **kwargs) -> str:
        """
        :param prompt:
        :param stop:
        :return:
        """

        print("Prompt:\n", prompt)

        model = self.config["MODEL_VERSION"]
        messages = [
            # {"role": "system", "content": """You are a poetic assistant,
            # skilled in explaining complex programming concepts with creative flair."""},
            {"role": "user", "content": prompt}
        ]
        print(
            f"""{helper_functions.num_tokens_from_messages(messages, model)} prompt tokens
                counted by num_tokens_from_messages()."""
        )

        response = ""
        client = OpenAI(api_key=self.config["KEY"])
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            # temperature=int(self.config["TEMPERATURE"]),
        )
        response = completion.choices[0].message.content
        print(response)
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
