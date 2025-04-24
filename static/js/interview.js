
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let stream;
let recognition;
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const videoElement = document.getElementById('video-preview');
const answerDisplay = document.getElementById('answer-display');
const submitButton = document.getElementById('submitButton');
const answerForm = document.getElementById('answerForm');
const hiddenAnswerInput = document.getElementById('hiddenAnswer');
const webCamToggle = document.getElementById('webcamToggle');

const hasGetUserMedia = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
const hasSpeechRecognition = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

function init() {
    if (!hasGetUserMedia) {
        alert('Your browser does not support webcam access');
        disableVideoFeatures();
    }
    
    if (!hasSpeechRecognition) {
        alert('Your browser does not support speech recognition');
        disableSpeechFeatures();
    }
    
    if (recordButton) recordButton.addEventListener('click', startRecording);
    if (stopButton) stopButton.addEventListener('click', stopRecording);
    if (webCamToggle) webCamToggle.addEventListener('change', toggleWebcam);
    if (answerForm) answerForm.addEventListener('submit', handleSubmit);
    
    if (stopButton) stopButton.disabled = true;
    
    setupSpeechRecognition();
}

async function toggleWebcam() {
    if (webCamToggle.checked) {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: true, 
                audio: true 
            });
            videoElement.srcObject = stream;
            videoElement.play();
            setupMediaRecorder();
            recordButton.disabled = false;
        } catch (err) {
            console.error('Error accessing media devices:', err);
            alert('Unable to access webcam or microphone');
            webCamToggle.checked = false;
        }
    } else {
        stopMediaTracks();
        videoElement.srcObject = null;
        recordButton.disabled = true;
        stopButton.disabled = true;
    }
}

function setupSpeechRecognition() {
    if (!hasSpeechRecognition) return;
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    
    // Handle results
    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = 0; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        
        // Update answer display and hidden input
        answerDisplay.textContent = transcript;
        hiddenAnswerInput.value = transcript;
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
    };
}

// Set up media recorder
function setupMediaRecorder() {
    if (!stream) return;
    
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };
}

// Start recording
function startRecording() {
    if (!mediaRecorder) return;
    
    audioChunks = [];
    mediaRecorder.start();
    
    if (recognition) {
        recognition.start();
    }
    
    isRecording = true;
    recordButton.disabled = true;
    stopButton.disabled = false;
}

// Stop recording
function stopRecording() {
    if (!mediaRecorder || !isRecording) return;
    
    mediaRecorder.stop();
    
    if (recognition) {
        recognition.stop();
    }
    
    isRecording = false;
    recordButton.disabled = false;
    stopButton.disabled = true;
    
    // Save the transcribed text
    saveTranscribedText();
}

// Save transcribed text via AJAX
function saveTranscribedText() {
    const interviewId = answerForm.dataset.interviewId;
    const questionNum = answerForm.dataset.questionNum;
    const answerText = hiddenAnswerInput.value;
    
    fetch(`/interview/${interviewId}/save_answer`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            question_num: questionNum,
            answer_text: answerText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Answer saved successfully');
        }
    })
    .catch(error => {
        console.error('Error saving answer:', error);
    });
}

// Handle form submission
function handleSubmit(e) {
    // Ensure answer is saved
    if (hiddenAnswerInput.value.trim() === '') {
        hiddenAnswerInput.value = answerDisplay.textContent;
    }
}

// Stop media tracks when closing/navigating away
function stopMediaTracks() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    
    if (isRecording) {
        stopRecording();
    }
}

// Disable video features
function disableVideoFeatures() {
    if (webCamToggle) webCamToggle.disabled = true;
    if (recordButton) recordButton.disabled = true;
    if (stopButton) stopButton.disabled = true;
}

// Disable speech features
function disableSpeechFeatures() {
    if (recordButton) recordButton.disabled = true;
    if (stopButton) stopButton.disabled = true;
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', init);