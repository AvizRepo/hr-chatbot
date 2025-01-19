const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const chatIcon = document.getElementById('chat-icon');
const chatContainer = document.getElementById('chat-container');

let isFirstMessage = true;

function addMessage(message, isUser) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage(message) {
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, initial: isFirstMessage }),
    })
    .then(response => response.json())
    .then(data => {
        addMessage(data.response, false);
        isFirstMessage = false;
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Error communicating with the server.', false);
    });
}

sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        sendMessage(message);
        userInput.value = '';
    }
});

userInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});

chatIcon.addEventListener('click', () => {
    chatContainer.style.display = 'block';

    if (isFirstMessage) {
        sendMessage('Hello there!');
    }
});