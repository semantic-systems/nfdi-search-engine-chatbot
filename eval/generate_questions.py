# -*- coding: utf-8 -*-
import json
import os
import time
from ast import literal_eval
from collections import defaultdict

import numpy as np
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from tqdm import tqdm

df = pd.read_csv(
    "search_results.csv",
    converters={
        "results": literal_eval,
        "bert_sim": literal_eval,
        "tfidf_sim": literal_eval,
        "bm25_sim": literal_eval,
    },
)

_ = load_dotenv(find_dotenv())


model = SentenceTransformer("all-MiniLM-L6-v2")

clusters = []
for results in tqdm(df.results):
    X = model.encode(results)
    if len(results) >= 50:
        kmeans = KMeans(n_clusters=10, random_state=0, n_init="auto").fit(X)
    else:
        kmeans = KMeans(n_clusters=5, random_state=0, n_init="auto").fit(X)

    clusters.append(kmeans.labels_)

df["k_mean_clusters"] = clusters

client = OpenAI(api_key=os.environ["OPENAI_KEY"])

gpt_responses = []
for sentences, labels in tqdm(zip(df.results, df.k_mean_clusters)):
    k_clusters = defaultdict(list)
    for res, label in zip(sentences, labels):
        # Assign title to corresponding cluster
        k_clusters[label].append(res)

    response_clusters = []
    for key, val in tqdm(k_clusters.items()):
        if len(val) <= 5:
            # Do not process if cluster contains less than 5 titles
            response_clusters.append(None)
            continue
        if len(val) > 5 and len(val) < 20:
            prompt = f"""The task is to generate questions based on provided information.
Given list of texts generate only two questions, no more than two questions.
Make questions variant.
The questions should imitate what a user might look for, in the given documents.

Return questions as Python list.

Documents:
{val}
"""
            sleep_count = 0
            while True:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4-1106-preview",
                        messages=[{"role": "assistant", "content": prompt}],
                    )
                    extracted_questions = response.choices[0].message.content
                    break
                except:
                    sleep_count += 1
                    if sleep_count >= 10:
                        extracted_questions = "NO QUESTIONS"
                        break
                    print("Going to sleep for 5 seconds!")
                    time.sleep(5)
            response_clusters.append(extracted_questions)
    gpt_responses.append(response_clusters)


df["gpt_questions"] = gpt_responses

df.to_csv("search_results_with_questions.csv", index=False)


def write_json(output_path, json_data):
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)


def gpt_cleaner(text):
    lst = eval(text)
    questions_lst = []
    for cluster_id, questions in enumerate(lst):
        if questions:
            if "```plaintext" in questions:
                questions = questions.replace("```plaintext", "").replace("```", "")
            if "```json" in questions:
                questions = questions.replace("```json", "").replace("```", "")
            if "```python" in questions:
                questions = questions.replace("```python", "").replace("```", "")
            if "\nquestions = [" in questions:
                questions = questions.replace("\nquestions = ", "")
            if "\n[" in questions:
                questions = questions.replace("\n[", "[")
            if "[\t" in questions:
                questions = questions.replace("[\t", "[")
            if "```" in questions:
                questions = questions.replace("```", "")
            try:
                questions_lst.append(
                    {"cluster_id": cluster_id, "questions": eval(questions)}
                )
            except:
                if len(questions.split("\n")) != 2:
                    questions_lst.append(
                        {"cluster_id": cluster_id, "questions": "No-Question"}
                    )
                else:
                    questions_lst.append(
                        {"cluster_id": cluster_id, "questions": questions.split("\n")}
                    )
        else:
            questions_lst.append({"cluster_id": cluster_id, "questions": "No-Question"})
    return questions_lst


data = []
for (
    search_key,
    elapsed_time,
    publications,
    resources,
    others,
    results_num,
    results,
    tfidf_sim,
    bert_sim,
    bm25_sim,
    k_means_clusters,
    gpt_q,
) in zip(
    df["search_key"],
    df["elapsed_time"],
    df["publications"],
    df["resources"],
    df["others"],
    df["results_num"],
    df["results"],
    df["tfidf_sim"],
    df["bert_sim"],
    df["bm25_sim"],
    df["k_mean_clusters"],
    df["gpt_questions"],
):
    data_dict = {
        "search_key": search_key,
        "elapsed_time": elapsed_time,
        "results_num": results_num,
    }
    results_lst = []
    for result, cosine_sim, bert_similarity, bm25_similarity, cluster_id in zip(
        eval(results),
        eval(tfidf_sim),
        eval(bert_sim),
        eval(bm25_sim),
        eval(k_means_clusters.replace(" ", ",").replace(",,", ",").replace("[,", "[")),
    ):
        results_lst.append(
            {
                "result": result,
                "cosine_sim": cosine_sim,
                "bert_sim": bert_similarity,
                "bm25_sim": bm25_similarity,
                "cluster_id": cluster_id,
            }
        )

    data_dict["GPT4-Questions"] = gpt_cleaner(gpt_q)
    # for
    # if len(gpt_cleaner(gpt_q)) != 2:
    #     print(gpt_cleaner(gpt_q))
    data_dict["results"] = results_lst
    data.append(data_dict)

write_json("search_results_sim_aiqa.json", data)
