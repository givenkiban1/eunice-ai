# Eunice AI

## Overview

Eunice AI is a customer support AI Agent developed by the Catalyst Labs team. Our aim is to provide effective and efficient support for customers through advanced AI technologies.

Eunice AI is built to enable phone calls to have the same impact as websites, at a fraction of the cost. This is important for SMEs in the service industry which is saturated e.g plumbing , garderning. 

These businesses get majority of their business leads telephonically as customer tend to search "<name> near me contact details", and do not want to search for hours across multiple vendors to hire, they much prefer calling 10 numbers to get the best quote and informaiton. 

## Access to live project 
URL : https://170.64.163.218/app

**Note** The url will only be live between Tuesday (6 Aug)  and Friday (9 Aug)

## Technologies Used

- **Python**: The primary programming language for the backend.
- **Flask**: A lightweight WSGI web application framework used for building the API.
- **Langchain**: A framework that enhances our language understanding and processing capabilities.
- **Deepgram**: Utilized for advanced speech recognition and transcription.
- **Groq**: A platform that hosts LLMs used for creating agents and querying.
- **Tavily**: A platform to manage and deliver conversational experiences.
 
## Features

- Intelligent customer support interactions.
- 24/7 availability to assist customers.
- Continuous learning from interactions to improve responses.
- Multi-channel support capabilities.
- Speech to text streaming
- Text to speech

## Installation

1. Clone the repository:
   `git clone https://github.com/givenkiban1/eunice-ai.git`

2. Create virtual environment (Conda or Venv)
```
# Create conda env ( you will need to confirm installation when running this command) 
conda create -n eunice-ai python=3.12

# Activate conda env
conda activate eunice-ai
```

3. Install dependencies:
   `pip install -r requirements.txt`

## Usage

4. Before you run the application, be sure to copy API Keys from `.env.example` and paste them in `.env` file with values in your root.

5. On 2 different terminals, run each of the following application with these commands: :
- Terminal 1: `python app.py` # Rest API

- Terminal 2: `python app_socketio.py` # websocket

7. Finally, access the application in your web browser at `http://localhost:8080`.
   
---
# Extra 

In a seperate repo, we built a telephonic integration and implementation of Eunice AI , where customer conversations and transcribed and processed by Eunice before speaking back all through your phone ( this is show in the demo video too) !! 

We are sharing this to also show the application of Euncie AI in different seetings `web application` ( as seen in this repo, which is our final submission) as well as in the following repo which has the `dialler/telephonic` integration. 

`eunice-ai-telephone repo:` https://github.com/eyespywmlileye/catalyst-labs-euniceAI-twilio 

## Contributing

We welcome contributions! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
