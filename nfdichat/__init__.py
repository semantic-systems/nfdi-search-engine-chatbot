# -*- coding: utf-8 -*-
"""
Root package of NFDI Search Engine ChatBot (nfdichat)
"""

__version__ = "0.1.0"

import logging

from nfdichat.common import configs, tools, util

__all__ = ["util", "configs", "tools"]


# Root logger configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stdout = logging.StreamHandler()
stdout.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
stdout.setFormatter(formatter)

logger.addHandler(stdout)
