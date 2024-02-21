# -*- coding: utf-8 -*-
""" Package for the LLMs component. """
from nfdichat.llms.openai import OpenAILLM
from nfdichat.llms.vicuna import VicunaLLM

__all__ = ["VicunaLLM", "OpenAILLM"]
