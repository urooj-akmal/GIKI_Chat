import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css'
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from "@chatscope/chat-ui-kit-react"



function App() {
  const [typing, setTyping] = useState(false);
  const [messages, setMessages] = useState([
    {
      message: "hello",
      sender: "api"
    }
  ]);

  const handleSend = (message) => {
    const newMessage = {
      message: message,
      sender: "User",
      direction: "outgoing"
    };
    setMessages([...messages, newMessage]);
    setTyping(true);
    processMessagetoAPI(message);
  };

  async function processMessagetoAPI(query) {
    const apiRequestBody = {
      Userid: '1258',
      query: query
    };
    const response = await fetch("http://localhost:8000/Chat_me", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(apiRequestBody)
    });

    if (!response.ok) {
      console.error('Error:', response.statusText);
      return;
    }

    const responseData = await response.json();
    const apiResponseMessage = responseData.response;

    const newMessage = {
      message: apiResponseMessage,
      sender: "API",
      direction: "incoming"
    };

    setMessages([...messages, newMessage]);
    setTyping(false);
  }
   return (
    <div className='App'>
      <div style={{ position: "relative", height : "800px", width: "700px"}}>
        <MainContainer>
          <ChatContainer>
            <MessageList
              typingIndicator={typing ? <TypingIndicator content="Model is typing"/>:null}
            >
              {messages.map((message,i) => {
                return <Message key={i} model={(message)} />
              })}
            </MessageList>
            <MessageInput placeholder='type your message here' onSend={handleSend}/>
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  )
}

export default App