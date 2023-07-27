# -*- coding: utf-8 -*-
"""
Includes help classes useful for encapsulating data.
"""
from typing import Any, Dict


class StrictDict(dict):
    """
    This class prevents adding new keys to the dictionary
    """

    def __setitem__(self, key: str, value: Any):
        self.check(key)
        dict.__setitem__(self, key, value)

    def update(self, __m: Dict[str, Any], **kwargs):
        for key, value in __m.items():
            self.check(key)

        for key, value in __m.items():
            self.__setitem__(key, value)

    def check(self, key: str):
        if key not in self:
            raise KeyError("{} is not a legal key of this StrictDict".format(repr(key)))
