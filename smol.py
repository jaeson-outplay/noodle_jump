import os
import shutil

from smolagents import CodeAgent, DuckDuckGoSearchTool, Tool, HfApiModel
from dotenv import load_dotenv, dotenv_values 
from tool import FindFilesTool, GitPushTool, FileUpdateTool

load_dotenv() 

HF_TOKEN = os.getenv("HF_TOKEN")

os.makedirs('./generatedImages', exist_ok=True)

image_generation_tool = Tool.from_space(
    "black-forest-labs/FLUX.1-schnell",
    name="image_generator",
    description="Generate an image from a prompt"
)

# reasoning_assistant_tool = Tool.from_space(
#     "webml-community/llama-3.2-reasoning-webgpu",
#     name="file_reason_assistant",
#     description="Tool to help in the assistance of logic",
#     token=HF_TOKEN
# )

model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct", token=HF_TOKEN)
"""
step 1: receive prompt
(deferred for now) step 2: analyze prompt for specific task (asset change, script change, etc) 
step 3: crawl files to search for specific file that matches task and save file location
step 4: run appropriate tool to accomplish task
step 5: upload changes to github
"""
find_files_tool = FindFilesTool()
file_replace_tool = FileUpdateTool()
agent = CodeAgent(tools=[find_files_tool, image_generation_tool, file_replace_tool], model=model)
# agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())
# Step 1: Prompt reception
response = agent.run("find me the webp file that is used to display trees in the level prop and replace it with a generated webp file of another retro bubbly style tree")
print(f"found asset: {response}")
# Run the agent to generate an image based on a prompt

# Assuming the response contains a URL to the generated image
image_path = os.path.normpath(response)
# Check if the image path exists
update_git_tool = GitPushTool()
agent = CodeAgent(tools=[update_git_tool], model=model)
agent.run("commit to new branch and push to repo", additional_args={'branch_name': 'image-replace-tool'})
