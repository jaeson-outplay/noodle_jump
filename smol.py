import os
import shutil

from smolagents import CodeAgent, DuckDuckGoSearchTool, Tool, HfApiModel
from dotenv import load_dotenv, dotenv_values 
from tool import FindFilesTool, GitPushTool, FileUpdateTool, ProcessFlowIdentifierTool

load_dotenv() 

HF_TOKEN = os.getenv("HF_TOKEN")

os.makedirs('./generatedImages', exist_ok=True)

image_generation_tool = Tool.from_space(
    "black-forest-labs/FLUX.1-schnell",
    name="image_generator",
    description="Generate an image from a prompt"
)

model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct", token=HF_TOKEN)
"""
Todo:
- prompt cleaning
- ensure github upload pathways
==============
step 1: receive prompt
(deferred for now) step 2: analyze prompt for specific task (asset change, script change, etc) 
step 3: crawl files to search for specific file that matches task and save file location
step 4: run appropriate tool to accomplish task
step 5: upload changes to github
"""
userPrompt = '"Can you change the cloud to something metroidvania style"'

find_files_tool = FindFilesTool()
file_replace_tool = FileUpdateTool()
process_identifier_tool=ProcessFlowIdentifierTool()

#Identify purpose of prompt
promptCleanerAgent = CodeAgent(tools=[process_identifier_tool], model=model)
instructions = promptCleanerAgent.run(f'determine the purpose of the following string "{userPrompt}" if it is one of the following: [asset_change, script_update]')
print("instructions: " + instructions)

appDescription = "This is an app that runs a 2d platformer game using Godot. Anything relating to the background can be found in the level folder. This includes backgrounds, platforms, and props (plants, etc). Anything related to the player can be found in the player folder. and anything related to the enemy is in the enemy folder. For asset changes make sure to look for webp files."
contextPrompt = f'using process_identifier_tool look for the appropriate instructions for "{instructions}" and apply it to the statement after this'
agent = CodeAgent(tools=[find_files_tool, image_generation_tool, process_identifier_tool, file_replace_tool], model=model)
response = agent.run(f"{appDescription} {contextPrompt} {userPrompt} ")
# agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())
# Step 1: Prompt reception
print(f"found asset: {response}")
# # Run the agent to generate an image based on a prompt
# # Check if the image path exists
update_git_tool = GitPushTool()
agent = CodeAgent(tools=[update_git_tool], model=model)
agent.run("commit to new branch and push to repo", additional_args={'branch_name': 'image-replace-tool-3'})
