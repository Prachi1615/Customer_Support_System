// Content of ChatHistory.js
import React from 'react';

function ChatHistory({ history }) {
    return (
        <div>
            {history.map((item, index) => (
                <div key={index}>
                    <strong>{item[0]}: </strong>{item[1]}
                </div>
            ))}
        </div>
    );
}

export default ChatHistory;
