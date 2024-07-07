from langchain_community.llms.ollama import Ollama
from langchain import hub
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import chainlit as cl
from langchain.embeddings import GPT4AllEmbeddings
from langchain.chains import RetrievalQA

CHROMA_PATH = "chroma"
DATA_PATH = "data"
QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-mistral")
DB_PATH = "vectorstores/db/"


def retrieval_qa_chain(llm, vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        return_source_documents=True)

    return qa_chain


def load_llm():
    llm = Ollama(
        model="mistral",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    return llm


def qa_bot():
    llm = load_llm()
    embedding = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf")
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embedding)
    qa = retrieval_qa_chain(llm, vectorstore)

    return qa


@cl.on_chat_start
async def start():
    chain = qa_bot()
    msg = cl.Message(content="Firing up the research info bot...")
    await msg.send()
    msg.content = "Hi, welcome to research info bot. What is your query?"
    await msg.update()
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message.content, callbacks=[cb])
    print(f"response: {res}")
    answer = res["result"]
    answer = answer.replace(".", ".\n")
    sources = res["source_documents"]

    if sources:
        answer += "Sources: " + str(str(sources))
    else:
        answer += "No Sources found"

    await cl.Message(content=answer).send()
