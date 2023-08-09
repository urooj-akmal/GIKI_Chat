from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from langchain.chains import ConversationChain

llama = LlamaAPI('LL-hEfnJLaXaugS9dD0VLks6mSORjtZgPFqiiLyI2pJcek4ByG8HqDZYC9FBIC90TRT')
chat_llama = ChatLlamaAPI(client=llama)

chatbot = ConversationChain(llm=chat_llama)

response = chatbot.run("Hello!")

print(response)
