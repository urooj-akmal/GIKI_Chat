from fastapi import FastAPI
from langchain.chains import ConversationalRetrievalChain
from pydantic import BaseModel
from llamaapi import LlamaAPI
from collections import defaultdict
from langchain_experimental.llms import ChatLlamaAPI

app = FastAPI(title="ConversationalRetrievalChainDemo")

llama = LlamaAPI('LL-hEfnJLaXaugS9dD0VLks6mSORjtZgPFqiiLyI2pJcek4ByG8HqDZYC9FBIC90TRT')
chat_llama = ChatLlamaAPI(client=llama)


# Configure CORS settings

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # Update this to your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def create_chain():
    from langchain.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings()

    from langchain.vectorstores import FAISS
    db = FAISS.load_local("gikichat_faiss_index", embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    from langchain.memory import ConversationBufferWindowMemory
    memory=ConversationBufferWindowMemory(memory_key="chat_history", input_key="question", return_messages=True)

    from langchain.chains import ConversationalRetrievalChain
    return ConversationalRetrievalChain.from_llm(chat_llama,retriever,memory=memory)


chain = create_chain()
chat_history = defaultdict(list)


class ChatRequest(BaseModel):
    Userid: str
    query: str

@app.post("/Chat_me")
def chat_me(request: ChatRequest):
    # Extract the Userid and question from the request body
    Userid = request.Userid
    query = request.query
    result = chain({'question': query})
    chat_history[Userid].append((query, result['answer']))
    file1 = open("Chat_histories/{0}.txt".format(Userid), "a")  # append mode
    file1.write(query + " " + result['answer']+"\n")
    file1.close()
    return {"response": result['answer']}