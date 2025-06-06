let mediaRecorder;
let audioChunks = [];


const audioMediaConstraints = {
    audio: true,
    video: false
};

function toggleRecording() {
    const recordBtn = document.getElementById('record');
    const inputChat = document.getElementById("input");
    const outputChat = document.getElementById("output");
    // to start recording
    if (recordBtn.value === 'Record') {
        navigator.mediaDevices.getUserMedia(audioMediaConstraints)
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    
                    // Creates a fetch request and puts the blob in there
                    let formData = new FormData();
                    formData.append("audio", audioBlob);

                    // fetches the input from the transcibed audio
                    fetch("/transcribe", {
                        method: "POST",
                        body: formData
                    })
                    .then((response) => response.json())
                    .then((data) => {
                        inputChat.value += "\n\n" + data.output
                        
                        // Nests the AI output to put in the other side
                        fetch("/output_backend", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ input: data.output })
                        })
                        .then((response) => response.json())
                        .then((data) => {
                            const audio = new Audio("data:audio/mp3;base64," + data.audio);
                            audio.play();
                            outputChat.value += "\n\n" + data.output
                            
                        });
                    });

                    // Optional, used to test recording
                    // const audio = new Audio(audioURL);
                    // audio.controls = true;
                    // document.body.appendChild(audio);  // You could append this elsewhere in your UI
                    // audio.play();
            };
            mediaRecorder.start();
            recordBtn.value = 'Stop Recording';
        })
        .catch(err => {
            console.error('Mic access denied:', err);
            alert('Please allow microphone access to record.');
        });
    }
    else {
        // Stop recording
        mediaRecorder.stop();
        recordBtn.value = 'Record';
    }
}