# ChatBot "JARVIS" OpenAI Function calling

This is a Python ChatBot application that utilizes the OpenAI GPT-3.5-turbo model for intelligent conversations and various functions (OpenAI function call). It allows interactions through both voice and text, as well as integrations with APIs to provide useful information about the weather and internet searches.

## Table of Contents
1. [Introduction](#introduction)
2. [How to Use](#how-to-use)
3. [Modules](#modules)
    - [AppChatBot.py](#appchatbotpy)
    - [ChatBotBrain.py](#chatbotbrainpy)
    - [custom_actions.py](#customactionspy)
    - [function_actions.py](#functionactionspy)
    - [conf.py](#confpy)
4. [API Keys](#api-keys)
5. [License](#license)

## Introduction

The ChatBot is a virtual assistant that can perform various tasks, such as answering questions, providing weather information, and conducting web searches. It is highly configurable and can be used through both voice and text, depending on your preferences. Conversations in the section are stored so the chatbot remembers the last questions, limited to a certain number of tokens that can be defined.

The main concept is to have both "human" conversations and the ability to perform functions where the chat model decides when to use the functions. See [here](https://openai.com/blog/function-calling-and-other-api-updates) for more information.

## Linux Raspberry Pi and Windows
The project has been fully tested using the Raspberry Pi 4B, 8GB model, and a USB camera with built-in USB microphone function. On the Windows system, it has been tested on Windows 10, using the built-in audio capture of the Dell notebook.

## How to Use

1. Clone this repository to your local machine.

It is recommended to use a virtual environment to install the packages.

If you are using Linux / Raspberry Pi OS:

```bash
sudo apt-get install python3-venv
cd ~
python3 -m venv TALKASSISTGPT
cd ~/TALKASSISTGPT
source bin/activate
```

If you are using Windows:
Open PowerShell as an administrator inside the project folder. You must have permissions to execute the script.

Check if Python is installed.

```powershell
python --version
```

If it is not installed, install Python for Windows from the official website [here](https://www.python.org/downloads/).

```powershell
cd ~/TALKASSISTGPT
python3 -m venv env
cd env\Scripts
.\activate
```

After this, you should verify that you are within the virtual environment (env).

```powershell
(env) PS C:\Users\YOURPATH\TalkAssistGPT>
```

Install ffmpeg.

```powershell
winget install ffmpeg
```

Respond with "Y" when prompted. ffmpeg is required for the ElevenLabs module (optional).

Afterward:

2. Install the necessary Python libraries using `pip install -r requirements.txt`.
3. Configure the necessary API keys in the `.env` file (see [API Keys](#api-keys)).
4. Execute the `AppChatBot.py` file to start the ChatBot.

```powershell
(env) PS C:\YOURPATH\TalkAssistGPT> python AppChatBot.py
```

## Modules

### AppChatBot.py

This is the main file you should run to start the ChatBot. It manages user interaction and calls the appropriate functions to answer questions and perform actions.

### ChatBotBrain.py

This module is responsible for interacting with the OpenAI GPT-3.5 Turbo model. It processes user inputs, sends them to the model, and returns the responses.

### function_actions.py

This module complements `ChatBotBrain.py`, introducing advanced functions using OpenAI's Function Calling. This allows the ChatBot to automatically choose which function to execute based on user questions.

It is possible to check the current weather in any city using the free API from [OpenWeather](https://openweathermap.org/current). The function can also fetch the forecast for up to 5 days.

For up-to-date internet searches, the main tool is DuckDuckGO. However, the free API does not provide links, and when there is no return from this API, the SERPAPI is automatically called using Google Search [here](https://serpapi.com/). The latter can also be obtained with a monthly limit for free use. In any case, the main source of answers for the chat is the Chat GPT-3.5-turbo model for non-current questions.

### custom_actions.py

This file contains functions for human interaction, such as speech, listening, wake word recognition, initialization functions, and more. It is essential for enabling voice interaction with the ChatBot.

The wake word "jarvis" was used to call the ChatBot and initiate the conversation. The performance is very good, and the system remains on standby waiting. The API key is free and can be obtained [here](https://picovoice.ai/platform/porcupine/).

To listen to the language model's responses, gTTS (free) or ElevenLabs for human voice was used. The API key can be obtained [here](https://elevenlabs.io/speech-synthesis).

### conf.py

This file must be configured before using the application. You can choose the language (Portuguese or English) and set the speech algorithm, requiring an API key to use the `elevenlabs` algorithm. To use the text-to-speech gTTS from Google, no API is necessary. However, with ElevenLabs, it is possible to have "human" voice with higher quality. You can obtain a free API key with a limited number of tokens for testing.

## API Keys

To use all the functionalities of the ChatBot, you must set up the following API keys in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key to access the GPT-3.5 Turbo model.
- `OPENWEATHER_API_KEY`: Your OpenWeather API key to obtain weather information.
- `apikey_search`: (Optional) Your API key for conducting web searches using SERPAPI.
- `API_KEY_ELEVENLABS` (Optional): Your API key to use the `elevenlabs` speech algorithm.

Make sure to securely store these keys and add them to the `.env` file in the same folder.

## To Do

- Improve and consolidate language functions, including translation functions instead of having multiple methods for each language.
- Transcribe pre-recorded speeches in mp3 to English as well.

## License

This ChatBot application is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.