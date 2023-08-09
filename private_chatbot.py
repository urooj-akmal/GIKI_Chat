from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

llama = LlamaAPI('LL-hEfnJLaXaugS9dD0VLks6mSORjtZgPFqiiLyI2pJcek4ByG8HqDZYC9FBIC90TRT')
chat_llama = ChatLlamaAPI(client=llama)

template = """Assistant is a large language model trained by Meta.
Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on Ghulam Ishaq Khan Institute. assistant cannot As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on topics related Ghulam Ishaq Khan Institute.
Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on topics related Ghulam Ishaq Khan Institute. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{chat_history}
Human: {human_input}
Assistant:"""

prompt = PromptTemplate(input_variables=["chat_history", "human_input"], template=template)

embeddings = HuggingFaceEmbeddings()
db = FAISS.load_local("gikichat_faiss_index", embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})
memory=ConversationBufferWindowMemory(memory_key="chat_history", input_key="question", return_messages=True)
llm_chain = ConversationalRetrievalChain.from_llm(chat_llama, retriever, memory=memory)

user_name = input("Enter your name? ")
print("Personlized GIKI Chatbot")
print(f'''Hello! Nice to meet you {user_name}! I am your helpful assistant. How may I assist you today?
Enter 'exit', 'quit', or 'bye' to end the conversation.
Enter 'clear memory' to clear the conversation memory.''')

while True:

    user_input = input(f"{user_name}:")

    if user_input.lower() in ['exit', 'quit', 'bye']:
        response = "Goodbye! Have a nice day!"
        print(f"Assistant: {response}")
        break

    if user_input.lower() == 'clear':
        memory.clear()
        response = "Conversation memory has been cleared."
        print(f"Assistant: {response}")
        continue

    print("Thinking...")
    output = llm_chain({"question": user_input})

    print(f"Assistant: {output['answer']}")