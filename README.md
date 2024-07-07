## Table of Contents

- Introduction
- Installation
- Demo
## Introduction
This repository build RAG app use Langchain, Ollama and Chainlit to query a PDF file. This suitable for testing cause of the lower required setting of RAM.
## Installation
### 1. Clone the repository  
```
https://github.com/thehaodev/RAG_DEMO.git
```
### 2. Create and activate a virtual environment 
```
py -m venv .venv
.venv\Scripts\activate
```
### 3. Install the required dependencies 
```
pip install -r requirements.txt
```
### 4. Install Ollama.
Down load Ollama at https://ollama.com/ . Then run this to get mistral model
```
ollama pull mistral
```
## Demo
In this Demo I alredy have pdf in ./data to simple the code. So just put your pdf to ./data file for testing
First we create vectordatabase.
```
python run create_db.py
```
Then run chainlit UI
```
chainlit run rag.py
```
This a example result:
![result_rag](https://github.com/thehaodev/RAG_DEMO/assets/112054658/90584144-ca4e-48d8-91de-b4155ecddef1)

Note that my laptop has low RAM so I use this solution to demo RAG app. 
This result make me 5 minute to run cause it run through Ollama server. I'll update in the feature soon with another solution. 
