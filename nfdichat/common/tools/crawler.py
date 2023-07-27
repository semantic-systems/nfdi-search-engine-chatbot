# -*- coding: utf-8 -*-
from typing import Dict, List
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_page(url: str) -> str:
    """
        Get the text of the web page at the given URL
    :param url: web page url
    :return: return a string containing the content
    """
    """
    """
    fd = urlopen(url)
    content = fd.read()
    fd.close()
    return content.decode("utf8")


def crawl(url: str) -> Dict[str, List[str]]:
    """
        Get the text of the web page at the given URL
    :param url:
    :return:
    """
    content = get_page(url)
    soup = BeautifulSoup(content, "html.parser")
    result_container = soup.find_all("div", {"class": "result_container"})
    subjects = []
    result_container_str = str(result_container[0])
    for subject in result_container[0].find_all("summary"):
        if not str(subject.text).isspace():
            # print(subject, "\n", subject.text)
            subjects.append(subject)
            result_container_str = result_container_str.replace(str(subject), "DILEMA")
    url_content_dict = {}
    for title, contents in zip(subjects, result_container_str.split("DILEMA")[1:]):
        url_content_dict[title.text.strip()] = []
        splited_contents = (
            contents.split("</div>\n<li>")
            if len(contents.split("</div>\n<li>")) > 1
            else contents.split('<p class="url">')
        )
        for splited_content in splited_contents:
            cleaned_splited_content = (
                BeautifulSoup(splited_content, "html.parser")
                .text.strip()
                .replace("\n\n", "\n")
            )
            url_content_dict[title.text.strip()].append(cleaned_splited_content)
    return url_content_dict
