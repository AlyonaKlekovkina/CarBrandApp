let currentCar = '';
let recognition;

// Function to open the quiz modal and start listening
function startQuiz(carName, imageURL) {
    currentCar = carName;
    document.getElementById('feedback').innerText = '';
    document.getElementById('prompt-text').innerText = 'Please say the name of this car.';
    document.getElementById('modalImage').src = imageURL;
    document.getElementById('carModal').classList.add('active');
    startListening();
}

// Function to close the quiz modal
function closeQuiz() {
    document.getElementById('carModal').classList.remove('active');
    stopListening();
    document.getElementById('feedback').innerText = '';
}

// Function to start listening to the user's voice
function startListening() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Sorry, your browser does not support Speech Recognition.');
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US'; // Change to your desired language
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript.trim().toLowerCase();
        checkAnswer(transcript);
    };

    recognition.onerror = function(event) {
        document.getElementById('feedback').innerText = 'Error occurred in recognition: ' + event.error;
        speak('I didn\'t catch that. Please try again.');
        // Retry listening after an error
        setTimeout(startListening, 1000);
    };

    recognition.onend = function() {
        // Optionally handle when recognition ends without a result
    };
}

// Function to stop listening
function stopListening() {
    if (recognition) {
        recognition.stop();
    }
}

// Function to check the user's answer
function checkAnswer(answer) {
    if (answer === currentCar.toLowerCase()) {
        const successMessage = 'Good job! You correctly named ' + currentCar + '!';
        document.getElementById('feedback').innerText = successMessage;
        speak(successMessage);

        // Send POST request to add star
        fetch('/add_star', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ car_name: currentCar })
        })
        .then(response => response.json())
        .then(data => {
            if (data.stars !== undefined) {
                // Update the star count in the UI
                document.getElementById(`stars-${currentCar}`).innerText = data.stars;
            }
        })
        .catch(error => console.error('Error:', error));

        // Close the modal after a short delay
        setTimeout(closeQuiz, 2000);
    } else {
        const failureMessage = 'Try again!';
        document.getElementById('feedback').innerText = failureMessage;
        speak(failureMessage);
        // Automatically retry listening after a short delay
        setTimeout(startListening, 1000);
    }
}

// Function to handle speech synthesis for feedback
function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
}

// Close modal when clicking outside the content
window.onclick = function(event) {
    const modal = document.getElementById('carModal');
    if (event.target === modal) {
        closeQuiz();
    }
};

// Handle escape key to close modal
window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeQuiz();
    }
});
