import json
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data/discourse_data.json", "r") as f:
    discourse = json.load(f)

with open("data/course_data.json", "r") as f:
    course = json.load(f)

kb = discourse + course if isinstance(course, list) else discourse + [{"title": "Course Notes", "content": course}]

corpus = [entry["title"] + " " + entry["content"] for entry in kb]
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

def answer_question(question: str):
    q_embedding = model.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(q_embedding, corpus_embeddings, top_k=2)[0]

    best_answers = []
    for hit in hits:
        entry = kb[hit['corpus_id']]
        best_answers.append({
            "url": entry.get("url", ""),
            "text": entry["content"][:300].strip() + "..."
        })

    return {
        "answer": best_answers[0]["text"],
        "links": best_answers
    }
