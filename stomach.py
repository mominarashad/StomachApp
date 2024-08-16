import streamlit as st
import anthropic
import os

# Initialize Claude client with your API key
api_key = os.getenv("ANTHROPIC_API_KEY")  # Use environment variable for API key
client = anthropic.Anthropic(api_key=api_key)


# Function to generate meal plans using Claude API based on user inputs
def generate_meal_plan(symptoms, diagnosis, allergies, dietary_preferences, activity_level, pain_level, stress_level, food_dislikes, restricted_foods):
    prompt = (
        f"Create a daily meal plan for a patient with the following details:\n\n"
        f"Symptoms: {symptoms}\n"
        f"Diagnosis: {diagnosis}\n"
        f"Allergies: {allergies}\n"
        f"Dietary Preferences: {dietary_preferences}\n"
        f"Activity Level: {activity_level}\n"
        f"Pain Level: {pain_level}\n"
        f"Stress Level: {stress_level}\n"
        f"Food Dislikes: {food_dislikes}\n"
        f"Restricted Foods: {restricted_foods}\n\n"
        f"Please provide a meal plan for Morning, Lunch, and Dinner that is suitable for the patient's condition."
    )

    # Call Claude API
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="You are a world-class nutritionist specializing in stomach-related conditions.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    # Extract and format the response
    meal_plan = message.content[0].text if message.content else "No meal plan generated. Please try again."
    return meal_plan

def main():
    st.set_page_config(page_title="GastroGuide", layout="wide")
    
    # Title and description about the app
    st.title("GastroGuide")
    st.markdown("""
        **GastroGuide** is designed to help individuals manage their stomach-related conditions by providing personalized meal plans. 
        Whether you're dealing with gastritis, ulcers, or other stomach issues, this app tailors your daily meals to support better digestive health.
        By considering your symptoms, dietary restrictions, and lifestyle, GastroGuide offers balanced meal plans for morning, lunch, and dinner, 
        ensuring you eat foods that are gentle on your stomach while still being nutritious.
    """)
    
    with st.sidebar:
        st.header("Personalize Your Meal Plan")
        st.markdown("Input your details below to receive a customized meal plan:")
        symptoms = st.text_area("Current Symptoms", "E.g., bloating, acid reflux, indigestion")
        diagnosis = st.selectbox("Stomach Condition Diagnosis", ["Gastritis", "Ulcers", "IBS", "None", "Other"])
        allergies = st.text_area("Allergies & Intolerances", "E.g., lactose, gluten, nuts")
        dietary_preferences = st.multiselect("Dietary Preferences", ["Vegetarian", "Vegan", "Gluten-free", "None"])
        activity_level = st.selectbox("Daily Activity Level", ["Sedentary", "Moderately Active", "Very Active"])
        pain_level = st.slider("Current Pain/Discomfort Level", 1, 10, 5)
        stress_level = st.slider("Current Stress Level", 1, 10, 5)
        food_dislikes = st.text_area("Food Dislikes", "E.g., spicy food, dairy products")
        restricted_foods = st.text_area("Restricted Foods (by doctor)", "E.g., citrus, caffeine, fried foods")
        
        generate_plan_btn = st.button("Generate Meal Plan")

    if generate_plan_btn:
        with st.spinner("Creating your personalized meal plan..."):
            meal_plan = generate_meal_plan(symptoms, diagnosis, allergies, dietary_preferences, activity_level, pain_level, stress_level, food_dislikes, restricted_foods)
            
            st.subheader("Your Meal Plan")
            st.markdown(meal_plan)

if __name__ == "__main__":
    main()
