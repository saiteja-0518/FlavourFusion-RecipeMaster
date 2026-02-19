import streamlit as st
import random
import os
from google import genai

st.set_page_config(
    page_title="Flavour Fusion",
    layout="wide"
)

os.environ["GOOGLE_API_KEY"] = "AIzaSyDny0HA3X4WGclWB2xVdBYXjxhtijTsA1A"

client = genai.Client()

generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 3000
}

MODEL_NAME = "gemini-flash-latest"

def get_joke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why do Python programmers prefer snake_case? Because it's easier to read!",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why do programmers mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
        "Why did the computer get cold? It left its Windows open."
    ]
    return random.choice(jokes)

def recipe_generation(topic, word_count):
    try:
        st.write("⏳ **Generating your recipe...**")
        st.write(
            "While I work on creating your blog, here's a little joke to keep you entertained:\n\n"
            f"😂 **{get_joke()}**"
        )

        prompt = f"""
Write a detailed recipe blog on the topic "{topic}".

The blog MUST be approximately {word_count} words.
Do NOT summarize.
Write full-length detailed content.

Include:
- A catchy title
- A 1–2 paragraph introduction
- Ingredients list with quantities
- Step-by-step detailed cooking instructions
- Tips and variations
- Serving suggestions
- Conclusion

Ensure the content is long, detailed, and close to {word_count} words.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=generation_config
        )

        st.success("🎉 Your recipe is ready!")
        return response.text

    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None


st.title("🍽️ Flavour Fusion: AI-Driven Recipe Blogging")
st.write("Enter a recipe topic and choose the word count to generate an AI-powered recipe blog.")

topic = st.text_input("Enter recipe topic")
word_count = st.slider("Select word count", 200, 1200, 500)

if st.button("Generate Recipe"):
    if topic.strip() == "":
        st.warning("Please enter a recipe topic.")
    else:
        result = recipe_generation(topic, word_count)

        if result:
            st.markdown(result)

            # Show word count
            st.info(f"Generated approximately {len(result.split())} words.")

            # Download button
            st.download_button(
                label="⬇️ Download Recipe",
                data=result,
                file_name=f"{topic.replace(' ', '_')}_recipe.txt",
                mime="text/plain"
            )
