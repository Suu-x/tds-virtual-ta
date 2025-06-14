# tds-virtual-ta
FastAPI-based virtual TA for Tools in Data Science
# TDS Virtual TA – IIT Madras Project

A virtual assistant for the Tools for Data Science (TDS) course that answers student queries using FastAPI, semantic search, and content scraped from the official TDS course notes and Discourse forum threads.

## 🚀 Features

- Built with **FastAPI**
- Accepts a question via POST request
- Returns relevant answers from:
  - Course notes (`course_data.json`)
  - Discourse discussions (`discourse_data.json`)
- Uses **sentence-transformers** for semantic similarity
- Publicly deployed API (Render or similar)
- JSON output for integration/testing

## 📂 Project Structure


