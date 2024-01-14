import os

from langchain.llms import HuggingFaceHub
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter

# Set your Hugging Face Hub API token
os.environ["HUGGINGFACE_API_TOKEN"] = "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"

# Load the text from the .txt file
text_file_path = "book2.txt"  # Change to your .txt file path
with open(text_file_path, "r") as f:
    text = f.read()


# Choose a model from Hugging Face Hub
model_id = "facebook/bart-base"  # Replace with your desired model

# Create the language model
llm = HuggingFaceHub(repo_id=model_id, huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN"), task="text-generation")

# Create the Hugging Face embeddings
embeddings = HuggingFaceEmbeddings()


text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.create_documents(text)
# Create the FAISS vector store
db = FAISS.from_documents(texts, embeddings)

query = "What is autism"

chain = load_qa_chain(llm, chain_type="refine", refine_prompt=query)

docs = db.similarity_search(query)
chain.run(input_documents=docs, question=query)
