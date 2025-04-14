# symptom_checker.py

# List of common symptoms to look for
SYMPTOM_KEYWORDS = [
    "fever", "cough", "headache", "sore throat", "nausea", "fatigue",
    "chills", "runny nose", "sneezing", "shortness of breath", "body ache"
]

# Sample rules for symptom combinations
def check_condition(symptoms):
    if "fever" in symptoms and "cough" in symptoms:
        return "You may have the flu or COVID-19. Please monitor your symptoms and consider seeking medical advice."
    elif "headache" in symptoms and "sore throat" in symptoms:
        return "It could be a mild cold or sinus infection. Stay hydrated and rest."
    elif "nausea" in symptoms and "fatigue" in symptoms:
        return "These symptoms might point to food poisoning or a stomach bug."
    else:
        return "I'm not sure about your condition. Please consult a healthcare provider for a proper diagnosis."

# Extract symptoms from user input
def extract_symptoms(text):
    found_symptoms = [symptom for symptom in SYMPTOM_KEYWORDS if symptom in text.lower()]
    return found_symptoms

# Chatbot loop
def chatbot():
    print("👩‍⚕️ Hello! I'm your symptom checker bot. Describe your symptoms.")
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Take care! 👋")
            break

        symptoms = extract_symptoms(user_input)
        
        if symptoms:
            print(f"Bot: I detected these symptoms: {', '.join(symptoms)}")
            advice = check_condition(symptoms)
            print(f"Bot: {advice}")
        else:
            print("Bot: Hmm, I couldn't recognize any symptoms. Can you rephrase or be more specific?")

if __name__ == "__main__":
    chatbot()
