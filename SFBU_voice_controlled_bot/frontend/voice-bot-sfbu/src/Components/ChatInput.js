import React, { useState } from 'react';

function ChatInput({ onSubmit }) {
    const [inputText, setInputText] = useState('');

    const handleSubmit = () => {
        onSubmit(inputText);
        setInputText('');
    };

    return (
        <div>
            <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} />
            <button onClick={handleSubmit}>Send</button>
        </div>
    );
}

export default ChatInput;
