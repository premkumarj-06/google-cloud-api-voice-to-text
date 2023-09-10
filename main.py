
from __future__ import division
from six.moves import queue
from google.cloud import speech

from google.oauth2 import service_account

from fastapi import FastAPI, WebSocket

from fastapi.middleware.cors import CORSMiddleware


import re
import sys

from google.cloud import speech
from six.moves import queue
from google.oauth2 import service_account


app = FastAPI()

origins = [
    "http://127.0.0.1:5501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


buff = queue.Queue()

def fillbuffer(in_data):
        """Continuously collect data from the audio stream, into the buffer."""
        buff.put(in_data)

def generator():
            chunk = buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)

def listen_print_loop(responses)->str:
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)
            print("------returning transcript--------")
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break
            num_chars_printed = 0
            return transcript
    return ""

# def send_data_to_socket(transcribed_data):
#     return transcribed_data

RATE = 16000

@app.websocket("/language/{lang_id}/ws")
async def audio(websocket: WebSocket, lang_id:str):
    
    await websocket.accept()
    print("web socket connected")
    """
    Collects audio from the stream, writes it to buffer and return the output of Google speech to text
    """

    language_code = lang_id  # a BCP-47 language tag
    
    file_name = 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(file_name)
    client = speech.SpeechClient(credentials=credentials)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        # enable_automatic_punctuation = True,
        # enableSpokenEmojis = True,
        profanity_filter  = True,
        enable_spoken_punctuation = True,
        speech_contexts = [{
         "phrases":["premkumar@gmail.com", "ilavarasi@gmail.com", "arulmozhi@gmail.com", "email@gmail.com", "*@abc.com", "muthamizh@gmail.com", "@gmail.com", "@"],
         "boost": 10.0
         
        }]
    ) 

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    while True:
        
        try:
            data = await websocket.receive_bytes()
            print("received data")
            fillbuffer(data)
        except Exception as exp:
            print("Connection closed", exp)
            break
        audio_generator = generator()
        requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        transcribed_data:str = listen_print_loop(responses)
        print(transcribed_data)
        # transcribed_data = send_data_to_socket()
        await websocket.send_text(transcribed_data)
