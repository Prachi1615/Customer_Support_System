import React, { useState } from 'react';
import axios from 'axios';
import FileInput from './Components/Fileinput';
import Button from './Components/Button';
import ChatHistory from './Components/ChatHistory';
import ChatInput from './Components/ChatInput';

function App() {
    const [loadedFile, setLoadedFile] = useState(null);
    const [chatHistory, setChatHistory] = useState([]);

    const handleFileChange = (file) => {
        setLoadedFile(file);
        const formData = new FormData();
        formData.append('file', file);

        axios.post('http://localhost:5000/load_db', formData)
            .then(response => {
                console.log(response.data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };

    const handleClearHistory = () => {
        setChatHistory([]);
        axios.post('http://localhost:5000/clear_history')
            .then(response => {
                console.log(response.data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };

    const handleConversation = (query) => {
        axios.post('http://localhost:5000/conversation', { query })
            .then(response => {
                const { answer, chat_history } = response.data;
                setChatHistory(prevHistory => [...prevHistory, ...chat_history]); // Update chat history with response
                setChatHistory(prevHistory => [...prevHistory, { user: 'Bot', message: answer }]); // Add bot's response to chat history
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };

    return (
        <div>
            <h1>Chat App</h1>
            <FileInput onFileChange={handleFileChange} />
            <Button onClick={handleClearHistory} label="Clear History" />
            <ChatHistory history={chatHistory} />
            <ChatInput onSubmit={handleConversation} />
        </div>
    );
}

export default App;
