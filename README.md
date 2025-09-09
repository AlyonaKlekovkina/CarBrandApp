# CarBrandApp 🚗🔊

An interactive app for practicing **car brand recognition**.  
Built as a fun project for my son, it combines a simple UI with **voice recognition** using [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text), allowing the user to **say the name of a car brand** and get instant feedback.

---

## ✨ Features
- 🎙️ **Voice input with Whisper**: Say a car brand aloud, and the app transcribes it into text  
- 🚘 **Car brand recognition game**: Practice naming brands, check correctness, and improve vocabulary  
- 🎨 **Basic UI design**: A simple but functional interface to make interaction engaging  
- 💻 **Local execution**: Runs on your machine, no deployment/server needed  

---

## 🛠️ Tech Stack
- **Python 3.x**
- **Whisper API (OpenAI)** for speech-to-text  
- **Tkinter** (or your chosen UI framework) for the graphical interface  
- Standard Python libraries  

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/AlyonaKlekovkina/CarBrandApp.git
cd CarBrandApp
2. Set up environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Configure OpenAI
Make sure you have your OpenAI API key set up as an environment variable:

bash
Copy code
export OPENAI_API_KEY="your_api_key_here"
4. Run the app
bash
Copy code
python main.py
🎮 How It Works
The app displays a car brand (text or image).

The player says the brand name into the microphone.

Whisper API transcribes the audio into text.

The app checks if the spoken brand matches the target.

Feedback is displayed (correct/incorrect).


🔧 Customization
Add more car brands (extend the dataset).

Replace car images with logos for a more visual experience.

Adjust Whisper settings for different languages/accents.

Expand into a full quiz game with score tracking.

🤝 Why I Built This
I wanted to create a small but fun project for my son to practice car brand recognition and explore AI voice technologies in a playful way.
It’s a humble project, but it works — and I’m proud of making it from scratch.
