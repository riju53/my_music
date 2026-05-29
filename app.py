from transformers import pipeline
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms.base import LLM
import scipy.io.wavfile as wavfile
import torch

# Load Music Generation Model
music_generator = pipeline(
    "text-to-audio",
    model="facebook/musicgen-small",
    device=0 if torch.cuda.is_available() else -1
)

# Function to generate music
def generate_music(prompt):
    print(f"Generating music for: {prompt}")

    output = music_generator(
        prompt,
        forward_params={"do_sample": True}
    )

    audio = output["audio"][0]
    sampling_rate = output["sampling_rate"]

    output_file = "generated_music.wav"

    wavfile.write(output_file, rate=sampling_rate, data=audio)

    return f"Music generated successfully: {output_file}"

# Create LangChain Tool
music_tool = Tool(
    name="Music Generator",
    func=generate_music,
    description="Generate music from text prompts"
)

# Simple Custom LLM Wrapper
class DummyLLM(LLM):
    @property
    def _llm_type(self):
        return "dummy"

    def _call(self, prompt, stop=None):
        return prompt

# Initialize Agent
llm = DummyLLM()

agent = initialize_agent(
    tools=[music_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run Agent
response = agent.run(
    "Generate relaxing lo-fi music for studying"
)

print(response)