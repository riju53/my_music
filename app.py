import streamlit as st
from huggingface_hub import InferenceClient

# -----------------------------
# Hugging Face API Setup
# -----------------------------
HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵"
)

st.title("🎵 AI Music Generator")
st.write("Generate music from text prompts using Hugging Face AI")

# User Input
prompt = st.text_area(
    "Enter your music prompt",
    placeholder="Example: Relaxing piano music for meditation"
)

# Generate Button
if st.button("Generate Music"):

    if prompt.strip() == "":
        st.warning("Please enter a music prompt.")

    else:
        with st.spinner("Generating music..."):

            try:
                # Generate Audio
                audio_bytes = client.text_to_audio(
                    prompt,
                    model="facebook/musicgen-small"
                )

                # Save Audio File
                output_file = "music.wav"

                with open(output_file, "wb") as f:
                    f.write(audio_bytes)

                st.success("Music generated successfully!")

                # Play Audio
                st.audio(output_file)

                # Download Button
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="Download Music",
                        data=file,
                        file_name="generated_music.wav",
                        mime="audio/wav"
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")
