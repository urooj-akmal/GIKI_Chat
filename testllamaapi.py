from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from langchain.chains import ConversationChain

llama = LlamaAPI('your-LLama-api-goes-here')
chat_llama = ChatLlamaAPI(client=llama)

chatbot = ConversationChain(llm=chat_llama)

response = chatbot.run("Hello!")

print(response)
