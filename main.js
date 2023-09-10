let recorder = null;
let socket = null;
let content = "";

function start_recording() {
  const selectElement = document.getElementById("region");
  const region = selectElement.value;

  const text_area_elem = document.getElementById("text_are_content");
  if (content != "" || text_area_elem.value.trim() != "") {
    content = "";
    selectElement.value = "";
  }
  if (socket != null) {
    socket.close();
  }
  socket = new WebSocket(`ws://localhost:8000/language/${region}/ws`);

  socket.onopen = () => {
    console.log("Connection is open now ----- socket");
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        recorder = new RecordRTC(stream, {
          type: "audio",
          mimeType: "audio/webm", // endpoint requires 16bit PCM audio
          sampleRate: 44100,
          desiredSampRate: 16000,
          recorderType: StereoAudioRecorder,
          numberOfAudioChannels: 1,
          timeSlice: 4000,
          ondataavailable: (blob) => {
            if (socket) {
              console.log(blob);
              socket.send(blob);
            }
          },
        });

        recorder.startRecording();
      })
      .catch((err) => console.error(err));
  };

  socket.onmessage = (message) => {
    content += " " + message.data;
    const selectElement = document.getElementById("text_are_content");
    selectElement.innerText = content;
  };
}

function stop_recording() {
  if (recorder != null) {
    recorder.stopRecording();
    content = " ";
  }
  if (socket != null) {
    socket.close();
  }
}
