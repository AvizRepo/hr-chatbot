# HR Chatbot

This project implements a simple HR chatbot for TechVed, as part of a coding assignment. The chatbot is designed to answer basic HR-related questions and handle leave requests.

## Prerequisites

*   **Node.js and npm:**  Make sure you have Node.js (version 16 or higher) and npm installed on your system. You can download them from [https://nodejs.org/](https://nodejs.org/).
*   **Python 3:** You need Python 3 (version 3.7 or higher) installed. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

## Setup and Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd techved-hr-chatbot
    ```

2. **Install Node.js dependencies:**

    ```bash
    npm install
    ```

3. **Install Python dependencies:**

    ```bash
    cd chatbot
    pip install -r requirements.txt
    ```

## Running the Chatbot

1. **Start the Node.js server:**

    ```bash
    node server.js
    ```

    The server will start on port 3000.

2. **Access the chatbot:**

    Open your web browser and go to `http://localhost:3000`. Click on the chat icon in the bottom-right corner to interact with the chatbot.

## Testing the Chatbot

To test the chatbot, open the chat interface in your browser and try the following:

1. **Ask predefined HR questions:**

    *   "How many leaves do I have left?"
    *   "What is the work-from-home policy?"
    *   "What is the procedure for applying for leave?"
    *   "When is the payroll disbursed?"

2. **Submit a leave request:**

    *   "I want to take leave from 2024-05-10 to 2024-05-15" (or use natural language like "I want to take leave from May 10th to May 15th").
    *   Confirm the leave request by typing "yes".

    The leave request will be simulated and the details will be written to the `leave_requests.txt` file.
