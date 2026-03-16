import openai
import speech_recognition as sr
import pyttsx3

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        print("Could not request results.")
        return ""

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if available
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = listen()
        if user_input:
            if "exit" in user_input.lower():
                speak("Goodbye!")
                break
            answer = ask_openai(user_input)
            print(f"Jarvis: {answer}")
            speak(answer)