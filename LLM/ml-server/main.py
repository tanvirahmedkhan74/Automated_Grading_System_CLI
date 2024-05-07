from fastapi import FastAPI
from transformers import AutoModelForCausalLM
from app import models
from pydantic import BaseModel
from typing import List

from sentence_transformers import SentenceTransformer

from milvus import default_server
from pymilvus import (
    connections,
    FieldSchema, CollectionSchema, DataType,
    Collection,
    utility
)

import re
import json

app = FastAPI()

"""Milvus Set Up"""
# star you milvus server
default_server.start()

_HOST = '127.0.0.1'
# The port may be changed, by default it's 19530
_PORT = default_server.listen_port

# Starting the connection
connections.connect(host=_HOST, port=_PORT)

# Schema and Collection Set Up
_DIMENSIONS = 384

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=_DIMENSIONS)
]

schema = CollectionSchema(fields=fields, enable_dynamic_field=True)

if utility.has_collection("vector_embed"):
    print("Found Existing Collection")
    collection = Collection(name="vector_embed")
else:
    print("Creating New Collection")
    collection = Collection(name="vector_embed", schema=schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 4}
    }

    collection.create_index(field_name="embedding", index_params=index_params)
collection.load()

# Embedding Model and Adding Data
transformer = SentenceTransformer('all-MiniLM-L12-v2')

text_classification_model = models.Assessment("google/gemma-2b-it",
                                              AutoModelForCausalLM, "text-generation")


class RubricAssessmentReq(BaseModel):
    criteria: str
    context: str
    prompt: str


class SingleAssessment(BaseModel):
    criteria: str
    context: str


class RagAssessment(BaseModel):
    criteria: str
    solution: str


class VectorEmbed(BaseModel):
    context: List[str]


@app.get("/")
async def root():
    question = "Explain priority inversion"
    answer = ("Priority inversion occurs in multitasking systems when a high-priority task gets stuck waiting for a "
              "resource held by a lower-priority task. Imagine a high-priority task (think processing urgent data) "
              "needs a tool (resource) that a low-priority task (like a background download) is currently using. "
              "Then, a medium-priority task (like checking email) comes along and preempts the low-priority task. "
              "Now, the high-priority task is stuck waiting for the medium-priority task to finish, even though it "
              "has a higher priority. This unexpected delay disrupts the intended order of tasks and can lead to "
              "performance issues.")
    # i = 1
    # for p in prompts:
    #     print(i)
    #     i += 1
    #     queue = f"{p} \n <Criteria>: {question} \n<Student's Solution>: {answer}"
    #     result = text_classification_model.gemma_rubric_assessment_cot(queue)

    return 200


@app.post("/rubric-assessment")
async def rubric_assessment(request: SingleAssessment):
    res = text_classification_model.rubric_assessment(request.criteria, request.context)
    return res


@app.get("/generate_results")
async def generate_w2_results():
    result = text_classification_model.generate_report_w2()
    return result


@app.get("/generate_results_w3")
async def generate_w3_results():
    result = text_classification_model.generate_report_w3()
    return result


@app.get("/generate_results_w7")
async def generate_w7_results():
    result = text_classification_model.generate_report_w7()
    return result


@app.post("/rag_gemma_assessment")
async def rag_gemma_assessment(request: RagAssessment):
    query_embedding = transformer.encode(request.criteria)
    res = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param={"metric_type": "L2",
               "params": {"nprobe": 2}},
        limit=5,
        output_fields=["sentence"]
    )

    context = []
    for i, hits in enumerate(res):
        for hit in hits:
            sen = hit.entity.get("sentence")
            context.append(sen)
            print(sen)

    print(context)
    result = text_classification_model.gemma_rag_assessment(request.criteria, request.solution, context)
    return result


@app.post("/add-embedded-data")
async def add_vector_embeddings(request: VectorEmbed):
    sentences = []
    for sentence in request.context:
        sentence.strip("\n")
        dot_split = sentence.split(".")

        for x in dot_split:
            sentences.append(x)
    # TODO Chunking
    # milvus input
    milvus_input = []
    for sentence in sentences:
        entry = {}
        vector_embedding = transformer.encode(sentence)
        entry["embedding"] = vector_embedding # {'the}
        entry["sentence"] = sentence
        milvus_input.append(entry)
        print(entry)

    collection.insert(milvus_input)
    collection.flush()

    return 200
