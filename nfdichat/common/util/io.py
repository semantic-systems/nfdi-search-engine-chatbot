# -*- coding: utf-8 -*-
"""
Includes Input/Output (I/O) functionalities like reading and writing from and into specific file formats.
"""
import json
import os
from typing import Any, Dict

import numpy as np

def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def create_dir(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def read_json(input_path: str) -> Dict[str, Any]:
    """
    Reads the ``json`` file of the given ``input_path``.

    :param input_path: Path to the json file
    :return: A loaded json object.
    """
    with open(input_path, encoding="utf-8") as f:
        json_data = json.load(f)

    return json_data


def write_json(output_path: str, json_data: Any):
    """
    Write the ``json_data`` to the ``output_path`` file.

    :param output_path:  Path to output json file
    :param json_data: A json Data
    :return:
    """
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)


def read_text(input_path: str) -> str:
    """
    Reads the ``text`` file of the given ``input_path``.

    :param input_path: Path to the text file
    :return:  A loaded text file.
    """
    with open(input_path, "r", encoding="utf8") as f:
        text = f.read()
    return text


def write_numpy_array(output_path: str, np_array: Any):
    """
    Write the ``np_array`` to the ``output_path`` file.

    :param output_path:  Path to output file
    :param np_array: A numpy array
    :return:
    """
    with open(output_path, "wb") as f:
        np.save(f, np_array)


def read_numpy_array(input_path: str) -> Any:
    """
    Reads the ``np_array`` file of the given ``input_path``.

    :param input_path: Path to the np_array file
    :return: A loaded nump array object.
    """
    with open(input_path, "rb") as f:
        return np.load(f)
