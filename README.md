# Customer Service Chatbot - ECommerce

## Overview
This project is a customer service chatbot built using Streamlit and Langchain. The chatbot is designed to assist users with inquiries related to orders, shipments, and other customer service needs.

## Features
- **Chat Interface**: A user-friendly chat interface for real-time interaction.
- **Session Management**: Unique session IDs to manage user interactions.
- **Chat History**: Maintains a history of conversations for context.
- **Agent Workflow**: Utilizes Langchain for processing user messages and generating responses.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd customer-service-chatbot
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables: Create a .env file in the root directory and define the necessary variables as specified in src/customer_service_chatbot/tools/settings.py.
Usage
To run the chatbot, execute the following command:

    ```bash
    cd src/customer_service_chatbot 
    streamlit run app.py 
    ```

## Code Structure
app.py: Main application file that initializes the Streamlit app and handles user interactions.
agent.py: Contains the logic for processing user messages and generating responses.
tools/: Directory containing various utility modules for settings, order details, and knowledge retrieval.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

### License
This project is licensed under the MIT License. See the LICENSE file for details