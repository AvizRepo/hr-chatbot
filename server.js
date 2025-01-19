const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.json());

app.use(express.static('public'));

const chatbotProcess = spawn('python', ['-u', 'chatbot/chatbot.py']);

const responses = {};
const sessions = {};

chatbotProcess.stdout.on('data', (data) => {
    const response = JSON.parse(data.toString());
    console.log("Chatbot response: " + JSON.stringify(response));

    const requestId = Object.keys(responses).find(
        (id) => responses[id].pending === true
    );
    if (requestId) {
        responses[requestId].res.json(response);
        responses[requestId].pending = false;
    }
});

chatbotProcess.stderr.on('data', (data) => {
    console.error('Chatbot error:', data.toString());
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/api/chat', (req, res) => {
    const userMessage = req.body.message;
    const userIP = req.ip;
    const requestId = Date.now().toString();
    console.log('Received message:', userMessage, 'Request ID:', requestId, 'IP:', userIP);

    responses[requestId] = { res, pending: true };

    if (req.body.initial || !sessions[userIP]) {
        const welcomeMessage = "Welcome to TechVed HR! I'm TechVed Assist, your virtual HR assistant. How can I help you today?";
        console.log("Sending welcome message");

        responses[requestId].res.json({ response: welcomeMessage });
        responses[requestId].pending = false;

        sessions[userIP] = { initialized: true };

        chatbotProcess.stdin.write('/start' + '\n');

    } else {
        chatbotProcess.stdin.write(userMessage + '\n' + userIP + '\n');
    }
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});