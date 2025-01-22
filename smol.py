import os
import shutil

from smolagents import CodeAgent, DuckDuckGoSearchTool, Tool, HfApiModel
from dotenv import load_dotenv, dotenv_values 
from tool import FindFilesTool, GitPushTool

load_dotenv() 

HF_TOKEN = os.getenv("HF_TOKEN")

os.makedirs('./generatedImages', exist_ok=True)

image_generation_tool = Tool.from_space(
    "black-forest-labs/FLUX.1-schnell",
    name="image_generator",
    description="Generate an image from a prompt"
)

model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct", token=HF_TOKEN)

find_files_tool = FindFilesTool()
agent = CodeAgent(tools=[image_generation_tool, find_files_tool], model=model)
# agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())

# Run the agent to generate an image based on a prompt
response = agent.run("Generate an image of a dog drawn in vector style")

# Assuming the response contains a URL to the generated image
image_path = os.path.normpath(response)
# Check if the image path exists
if os.path.exists(image_path):
    # Define the destination path for the saved image
    image_filename = os.path.join('./generatedImages', 'generated_image.webp')
#     # Create the './generatedImages' directory if it doesn't exist
    os.makedirs('./generatedImages', exist_ok=True)

#     # Copy the image from the temporary location to the desired directory
    shutil.copy(image_path, image_filename)

    print(f"Image saved to {image_filename}")
    update_git_tool = GitPushTool()
    agent = CodeAgent(tools=[update_git_tool], model=model)
    agent.run("commit to new branch and push to repo", additional_args={'branch_name': 'git-push-tool'})
else:
    print("Failed to generate an image or the file does not exist.")
