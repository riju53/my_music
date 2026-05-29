
import streamlit as st
import requests

# -----------------------------
# Hugging Face API Setup
# -----------------------------
API_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵"
)

st.title("🎵 AI Music Generator")

st.write("Generate music from text prompts using Hugging Face")

prompt = st.text_area(
    "Enter your music prompt",
    placeholder="Example: Relaxing piano music for meditation"
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate Music"):

    if prompt.strip() == "":
        st.warning("Please enter a music prompt.")

    else:
        with st.spinner("Generating music..."):

            try:

                payload = {
                    "inputs": prompt
                }

                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload
                )

                # Check API response
                if response.status_code != 200:
                    st.error(f"API Error: {response.text}")

                else:
                    output_file = "music.wav"

                    # Save audio
                    with open(output_file, "wb") as f:
                        f.write(response.content)

                    st.success("Music generated successfully!")

                    # Play audio
                    st.audio(output_file)

                    # Download button
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="Download Music",
                            data=file,
                            file_name="generated_music.wav",
                            mime="audio/wav"
                        )

            except Exception as e:
                st.error(f"Error: {str(e)}")
