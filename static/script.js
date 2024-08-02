let isRecording = false;
let socket;
let microphone;
const PLAY_STATES = {
  NO_AUDIO: "no_audio",
  LOADING: "loading",
  PLAYING: "playing",
};

let playState = PLAY_STATES.NO_AUDIO;
let audio;

const socket_port = 5001;
socket = io(
  "http://" + window.location.hostname + ":" + socket_port.toString()
);

socket.on("transcription_update", (data) => {
  document.getElementById("captions").innerHTML = data.transcription;
  document.getElementById("captions_2").innerHTML = data.output_text;

  // make call to llm to get a response
  sendData(data.output_text);
});

async function getMicrophone() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    return new MediaRecorder(stream, { mimeType: "audio/webm" });
  } catch (error) {
    console.error("Error accessing microphone:", error);
    throw error;
  }
}

async function openMicrophone(microphone, socket) {
  return new Promise((resolve) => {
    microphone.onstart = () => {
      console.log("Client: Microphone opened");
      document.body.classList.add("recording");
      resolve();
    };
    microphone.ondataavailable = async (event) => {
      console.log("client: microphone data received");
      if (event.data.size > 0) {
        socket.emit("audio_stream", event.data);
      }
    };
    microphone.start(1000);
  });
}

async function startRecording() {
  isRecording = true;
  microphone = await getMicrophone();
  console.log("Client: Waiting to open microphone");
  await openMicrophone(microphone, socket);
}

async function stopRecording() {
  if (isRecording === true) {
    microphone.stop();
    microphone.stream.getTracks().forEach((track) => track.stop()); // Stop all tracks
    socket.emit("toggle_transcription", { action: "stop" });
    microphone = null;
    isRecording = false;
    console.log("Client: Microphone closed");
    document.body.classList.remove("recording");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const recordButton = document.getElementById("record");

  recordButton.addEventListener("click", () => {
    if (!isRecording) {
      socket.emit("toggle_transcription", { action: "start" });
      startRecording().catch((error) =>
        console.error("Error starting recording:", error)
      );
    } else {
      stopRecording().catch((error) =>
        console.error("Error stopping recording:", error)
      );
    }
  });
});

function sendData(textInput) {
  const modelSelect = document.getElementById("models");
  const selectedModel = modelSelect.options[modelSelect.selectedIndex].value;
  if (!textInput) {
    errorMessage.innerHTML = "ERROR: Please add text!";
  } else {
    playState = PLAY_STATES.LOADING;

    const data = {
      model: selectedModel,
      text: textInput,
    };
    fetch("http://localhost:8080/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        playState = PLAY_STATES.PLAYING;

        // Check if there's an existing audio source and stop it
        stopAudio();

        // Create a Blob from the response data
        return response.blob();
      })
      .then((blob) => {
        // Create an object URL from the Blob
        const audioUrl = URL.createObjectURL(blob);

        // Create an audio element and play the audio URL
        const audioPlayer = document.getElementById("audio-player");
        audioPlayer.src = audioUrl;
        audioPlayer.play();

        audioPlayer.addEventListener("ended", () => {
          playState = PLAY_STATES.NO_AUDIO;
        });
      })
      .catch((error) => {
        console.error("Error fetching audio:", error);
        playState = PLAY_STATES.NO_AUDIO;
      });
  }
}

// Function to play audio
function playAudio(audioUrl) {
  if (audio) {
    stopAudio();
  }
  currentAudioUrl = audioUrl + "?t=" + new Date().getTime(); // Add cache-busting query parameter
  audio = new Audio(currentAudioUrl);

  audio.play();

  audio.addEventListener("ended", () => {
    console.log("Audio finished playing");
    stopAudio();
  });
}

// Function to stop audio
function stopAudio() {
  if (audio) {
    audio.pause();
    audio.currentTime = 0;
    playState = PLAY_STATES.NO_AUDIO;
  }
}
