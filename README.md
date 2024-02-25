# The Office ChatBot
This repository contains two Python scripts that work together to create a ChatBot dedicated to answering questions about the American TV series "The Office."

## File 1: Web Scraping and Database Creation
### Script Name: part 3.ipynb
The name is such because it was part of a college assignment hence it made it easier for me to keep track
### Overview
This notebook performs the following tasks:

Extracts links to Wikipedia pages containing information about each episode of "The Office" from a specified Wikipedia page.
Scrapes the content of these Wikipedia pages, extracts paragraphs, and creates a single string variable containing all the scraped information.
Utilizes the LangChain library to split the text into chunks and create a database (Chroma) with OpenAI embeddings.

### Usage
Run the notebook.
The script will output progress messages as it processes the Wikipedia pages and create the database.
The final database is saved in the "db" directory.

## File 2: Streamlit ChatBot Interface
### Script Name: streamlit_chatbot.py
### Overview
This script implements a Streamlit-based interface for the ChatBot. It utilizes the created database to answer user queries about "The Office" and provides relevant YouTube video links.

### Usage
Make sure the required dependencies are installed (streamlit, langchain, langchain_google_genai, google-api-python-client, yaml, requests, bs4).
Run the script with the command streamlit run streamlit_chatbot.py.
Interact with the ChatBot by typing questions about "The Office" in the provided chat input.
### Features
Provides prompts for common questions about "The Office."
Utilizes LangChain for similarity search in the database.
Generates relevant YouTube video links based on user queries.
## Note
The script requires an API key for OpenAI, Gemini, and YouTube - which I have provided, but it might run out of credits very soon. Make sure to provide these keys in a YAML file named myauth.yaml when you want to use your own. 
Feel free to explore and enhance the functionalities of these scripts to create an even more interactive and informative ChatBot for "The Office."
