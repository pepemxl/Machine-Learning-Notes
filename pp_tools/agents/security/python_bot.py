from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
import os
import pinecone
from pp_tools.common.constants import AGENTS_SECURITY_PATH
from pp_tools.common.environment_variables import get_env_var


HUGGINGFACE_API_TOKEN = get_env_var("HUGGINGFACE_API_TOKEN")
PINECONE_API_KEY = get_env_var("PINECONE_API_KEY")


class ChatBot():
    TEST_AGENT_DATA = os.path.join(AGENTS_SECURITY_PATH, "test.txt")
    loader = TextLoader(TEST_AGENT_DATA)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
    docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings()

    pinecone.init(
        api_key= os.getenv('PINECONE_API_KEY'),
        environment='gcp-starter'
    )

    index_name = "langchain-demo"

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric="cosine", dimension=768)
        docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    else:
        docsearch = Pinecone.from_existing_index(index_name, embeddings)

    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.8, "top_p": 0.8, "top_k": 50}, huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_TOKEN')
    )

    from langchain import PromptTemplate

    template = """
    You are a cybersecurty expert. These Human will ask you a questions about cybersecurity. Use following piece of context to answer the question. 
    If you don't know the answer, just say you don't know. 
    You answer with short and concise answer, no longer than 2 sentences.

    Context: {context}
    Question: {question}
    Answer: 

    """

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    

    rag_chain = (
        {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
        | prompt 
        | llm
        | StrOutputParser() 
    )