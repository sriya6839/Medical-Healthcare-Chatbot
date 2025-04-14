import os

from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline

## Load environment variables for Hugging Face token


# Step 1: Setup LLM (Replace with BioClinicalBERT)
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")  # Ensure your Hugging Face token is set
BERT_MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"

def load_bert_llm(model_name):
    # Use Hugging Face's pipeline for text generation or question-answering
    qa_pipeline = pipeline(
        "question-answering",
        model=model_name,
        tokenizer=model_name
    )
    llm = HuggingFacePipeline(pipeline=qa_pipeline)
    return llm

# Step 2: Connect LLM with FAISS and Create chain

CUSTOM_PROMPT_TEMPLATE = """
Refer exclusively to the provided context to answer the user's question.
If the answer is not present in the context, respond with "I don't know." Avoid making up answers or providing information beyond what is given.

Context: {context}
Question: {question}

Respond directly to the question without any introductory remarks.
"""

def set_custom_prompt(custom_prompt_template):
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt

# Load FAISS Database
DB_FAISS_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=load_bert_llm(BERT_MODEL_NAME),
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=True,
    chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
)

# Now invoke with a single query
user_query = input("Write Query Here: ")
response = qa_chain.invoke({'query': user_query})
print("RESULT: ", response["result"])
#print("SOURCE DOCUMENTS: ", response["source_documents"])