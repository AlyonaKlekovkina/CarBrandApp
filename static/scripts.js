let currentCar = '';
let mediaRecorder;
let audioChunks = [];
let quizActive = false; // Flag to track if the quiz is active
let mediaStream; // To store the media stream for proper closure

// Function to clean and normalize text
function cleanText(text) {
    return text
        .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "") // Remove punctuation
        .replace(/\s{2,}/g, " ") // Replace multiple spaces with single space
        .trim()
        .toLowerCase();
}

// Function to open the quiz modal and start listening
function startQuiz(carName, imageURL) {
    currentCar = carName;
    quizActive = true; // Set the quiz as active
    document.getElementById('feedback').innerText = '';
    document.getElementById('prompt-text').innerText = 'Please say the name of this car.';
    document.getElementById('modalImage').src = imageURL;
    document.getElementById('carModal').classList.add('active');
    startListening();
}

// Function to close the quiz modal
function closeQuiz() {
    quizActive = false; // Set the quiz as inactive
    document.getElementById('carModal').classList.remove('active');
    stopListening();
    document.getElementById('feedback').innerText = '';
}

// Function to start listening to the user's voice
async function startListening() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Sorry, your browser does not support audio recording.');
        return;
    }
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' }); // Use appropriate type
            audioChunks = [];
            // Only process transcription if the quiz is still active
            if (quizActive) {
                const transcript = await transcribeAudio(audioBlob);
                checkAnswer(transcript);
            }
        };
        // Stop recording after a set time (e.g., 5 seconds)
        setTimeout(() => {
            // Only stop if the quiz is still active
            if (quizActive && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
        }, 2500);
    } catch (error) {
        document.getElementById('feedback').innerText = 'Microphone access error: ' + error.message;
        speak('I didn\'t catch that. Please try again.');
        setTimeout(startListening, 1000);
    }
}

// Function to transcribe audio using your backend
async function transcribeAudio(audioBlob) {
    try {
        const formData = new FormData();
        formData.append('file', audioBlob, 'speech.wav'); // Use appropriate extension and type
        const response = await fetch('/transcribe', { // Ensure this path matches your Flask route
            method: 'POST',
            body: formData
        });
        console.log('Received response from /transcribe:', response);
        const data = await response.json();
        console.log('Transcription data:', data);
        if (response.ok) {
            return data.text.trim().toLowerCase();
        } else {
            throw new Error(data.error || 'Transcription failed');
        }
    } catch (error) {
        console.error('Transcription Error:', error);
        if (quizActive) { // Only provide feedback if the quiz is active
            document.getElementById('feedback').innerText = 'Transcription error: ' + error.message;
            speak('I\'m having trouble understanding. Please try again.');
            // Only restart listening if the quiz is still active
            setTimeout(startListening, 1000);
        }
        return '';
    }
}

// Function to stop listening
function stopListening() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    if (mediaStream) {
        // Stop all tracks to release the microphone
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
}

// Function to check the user's answer
const brandAliases = {
    "ferrari": ["феррари", "ferarri"],
    "chevrolet": ["шевроле", "шеврали", "шефрали"],
    "honda": ["хонда", "хонды"],
    "nissan": ["ниссан", "нисан", "new sun"],
    "volkswagen": ["фольксваген", "вольцваген", "вольфсваген", "vollzweigen", "vollzeugen"],
    "mercedes-benz": ["мерседес", "мерседес-бенц", "мерс", "Мерседес-Бенз"],
    "toyota": ["тойота"],
    "bmw": ["бмв", "биммер"],
    "audi": ["ауди", "Aude"],
    "ford": ["форд", "форт", "4th", "Forte"],
    // add more as needed
};

// --- Normalize brand name (canonical form) ---
function normalizeBrand(word) {
    for (const [canonical, aliases] of Object.entries(brandAliases)) {
        if (word === canonical || aliases.includes(word)) {
            return canonical;
        }
    }
    return word;
}

// --- Simple Levenshtein distance ---
function levenshtein(a, b) {
    const dp = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));
    for (let i = 0; i <= a.length; i++) dp[i][0] = i;
    for (let j = 0; j <= b.length; j++) dp[0][j] = j;

    for (let i = 1; i <= a.length; i++) {
        for (let j = 1; j <= b.length; j++) {
            const cost = a[i - 1] === b[j - 1] ? 0 : 1;
            dp[i][j] = Math.min(
                dp[i - 1][j] + 1,      // deletion
                dp[i][j - 1] + 1,      // insertion
                dp[i - 1][j - 1] + cost // substitution
            );
        }
    }
    return dp[a.length][b.length];
}

function similarity(a, b) {
    const distance = levenshtein(a, b);
    const maxLen = Math.max(a.length, b.length);
    return 1 - distance / maxLen;
}

// --- Updated checkAnswer ---
function checkAnswer(answer) {
    if (!quizActive) return;

    const cleanedAnswer = normalizeBrand(cleanText(answer));
    const cleanedCarName = normalizeBrand(cleanText(currentCar));

    const sim = similarity(cleanedAnswer, cleanedCarName);

    if (cleanedAnswer === cleanedCarName || sim >= 0.7) {
        const successMessage = `Good job! You correctly named ${currentCar}!`;
        document.getElementById('feedback').innerText = successMessage;
        speak(successMessage);

        fetch('/add_star', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ car_name: currentCar })
        })
        .then(response => response.json())
        .then(data => {
            if (data.stars !== undefined) {
                document.getElementById(`stars-${currentCar}`).innerText = data.stars;
            }
        })
        .catch(error => console.error('Error:', error));

        setTimeout(closeQuiz, 2000);
    } else {
        const failureMessage = 'Try again!';
        document.getElementById('feedback').innerText = failureMessage;
        speak(failureMessage);
        setTimeout(startListening, 1000);
    }
}

// Function for speech synthesis
function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('carModal');
    if (event.target === modal) {
        closeQuiz();
    }
};

// Close modal on Escape key
window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeQuiz();
    }
});
