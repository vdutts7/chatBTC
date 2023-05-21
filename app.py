from langchain.llms import OpenAI
import streamlit as strmlt
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma

# Agentic search
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)
from utils import get_base64
from utils import set_background

import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_llm = OpenAI(api_key=openai_api_key, temperature=0.1, verbose=True)


loader = PyPDFLoader('bitcoin.pdf') # Create + load PDF Loader
pages = loader.load_and_split() # Split pages from pdf 
chroma_store = Chroma.from_documents(pages, collection_name='bitcoin') # Load document(s) into vector database aka ChromaDB


# Create vectorstore info object - metadata repo?
encoded_string = get_base64("_btc.png")
set_background("_btc.png")

vectorstore_info = VectorStoreInfo(
    name="bitcoin",
    description="The Official BTC Whitepaper by Satoshi Nakamoto [pdf] ",
    vectorstore=chroma_store
)
# Convert document store into Langchain toolkit
langchain_toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

# Add the toolkit to an end-to-end langchain
agent_craigwright = create_vectorstore_agent(
    llm=openai_llm,
    toolkit=langchain_toolkit,
    verbose=True
)

strmlt.title('GPT Satoshi')

# Create a text input box for the user
prompt = strmlt.text_input('Your path to freedom starts here. Congrats on taking the orange pill. Be patient and watch around you. ') + "if asked about Bitcoin's total supply, remember that it is fixed at 21 million total supply, meaning only 21 million entire Bitcoins can theoretically be mined and that's the upper limit of the supply. This can never change"

# If the user hits enter, feed prompt to LLM and print response
if prompt:
    response = agent_craigwright.run(prompt)
    strmlt.write(response)

    with strmlt.expander('Document Similarity Search'):
        search = chroma_store.similarity_search_with_score(prompt) 
        strmlt.write(search[0][0].page_content) 