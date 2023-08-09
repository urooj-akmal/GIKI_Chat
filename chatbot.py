from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from llamaapi import LlamaAPI
from pydantic import BaseModel
from collections import defaultdict
from langchain_experimental.llms import ChatLlamaAPI
from langchain import PromptTemplate


app = FastAPI(title="GikiChatbot")
templates = Jinja2Templates(directory="templates")

llama = LlamaAPI('your-LLama-api-goes-here')
chat_llama = ChatLlamaAPI(client=llama)

template = """Assistant is a large language model trained by Meta.
Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on Ghulam Ishaq Khan Institute. assistant cannot As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on topics related Ghulam Ishaq Khan Institute.
Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on topics related Ghulam Ishaq Khan Institute. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{chat_history}
Human: {human_input}
Assistant:"""

prompt = PromptTemplate(input_variables=["chat_history", "human_input"], template=template)


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
    Userid = request.Userid
    query = request.query
    result = chain({'question': query})
    chat_history[Userid].append((query, result['answer']))
    file1 = open("{0}.txt".format(Userid), "a")  # append mode
    file1.write(f"Human: {query} Assistant: {result['answer']}\n")
    file1.close()
    return {"response": result['answer']}


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
