let currentCar = '';
let stars = 0;

// Function to open the quiz modal
function startQuiz(carName) {
    currentCar = carName;
    document.getElementById('feedback').innerText = '';
    document.getElementById('prompt-text').innerText = 'Please say the name of this car.';
    document.getElementById('quiz-modal').style.display = 'block';
}

// Function to close the quiz modal
function closeQuiz() {
    document.getElementById('quiz-modal').style.display = 'none';
}

// Function to start listening to the user's voice
function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Sorry, your browser does not support Speech Recognition.');
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US'; // Change to 'ru-RU' if using Russian
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript.trim().toLowerCase();
        checkAnswer(transcript);
    }

    recognition.onerror = function(event) {
        document.getElementById('feedback').innerText = 'Error occurred in recognition: ' + event.error;
    }
}

// Function to check the user's answer
function checkAnswer(answer) {
    if (answer === currentCar.toLowerCase()) {
        stars += 1;
        document.getElementById('stars').innerText = stars;
        document.getElementById('feedback').innerText = 'Great job! You correctly named ' + currentCar + '!';
        // Optionally, add a star animation here
    } else {
        document.getElementById('feedback').innerText = 'Incorrect. This is ' + currentCar + '.';
        // Optionally, provide additional details about the car
    }
}
