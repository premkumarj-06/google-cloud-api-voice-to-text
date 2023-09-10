## Google Cloud API Voice to Text using Python

This project implements voice-to-text conversion using the Google Cloud API. It integrates a frontend built with vanilla JavaScript, HTML, and CSS and a backend implemented using FastAPI through a WebSocket connection. The communication between the frontend and backend is facilitated by WebRTC's RecordRTC functions.

### How it Works
The frontend receives input audio signals as byte data.
It sends this data to the backend (FastAPI) through a WebSocket connection.
The backend sends the byte data to the Google Cloud API for transcription.
The processed output, which is the transcribed text, is returned from the Google Cloud API.
The result is sent back to the frontend through the same WebSocket connection.
The transcribed text is displayed on the frontend.
This project serves as a simple example of how voice-to-text can be integrated into a website. There are many more possibilities for expansion and improvement.

### Getting Started
To use this project, follow these steps:

Create a Google Cloud Platform (GCP) account for yourself.
Create a service account on GCP.
Download the service account credentials JSON file and replace it with the existing credentials.json file in this repository.
Run the main.py program file in the backend (FastAPI).
Open the index.html file in your web browser.
Allow microphone permission when prompted.
You're all set! Now you can transcribe voice recordings in the languages available in the dropdown menu.

### Additional Notes
Make sure to have a GCP account and service account for authentication.
This project is a basic demonstration and can be extended for more advanced features.
We hope you find this project useful and enjoyable. Happy coding!
Feel free to customize the formatting and content further to suit your preferences and project details.
