import os
import shutil
import subprocess

from smolagents import CodeAgent, DuckDuckGoSearchTool, Tool, HfApiModel
from dotenv import load_dotenv, dotenv_values 
from tool import FindFilesTool

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
    try:
        gitUsername = os.getenv("GIT_USERNAME")
        gitEmail = os.getenv("GIT_EMAIL")
        # Step 1: Ensure we are in a Git repository
        subprocess.run(["git", "status"], check=True)

        # Step 2: Create and switch to a new branch
        new_branch = "add-generated-image-2"
        subprocess.run(["git", "checkout", "-b", new_branch], check=True)
        print(f"Checked out to new branch: {new_branch}")

        # Step 3: Add the changes
        subprocess.run(["git", "add", "*"], check=True)
        print("Changes added to staging.")
        # Step 4: Add credentials
        subprocess.run(["git", "config", "--global", "user.email", gitEmail], check=True)
        print("Updated git email.")
        subprocess.run(["git", "config", "--global", "user.name", gitUsername], check=True)
        print("Updated git user name.")

        # Step 5: Commit the changes
        commit_message = "Add generated image to repository"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Changes committed.")

        #Step 6: Push the branch to the remote repository
        subprocess.run(["git", "push", "--set-upstream", "origin", new_branch], check=True)
        print(f"Branch '{new_branch}' pushed to remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while performing Git operations: {e}")
else:
    print("Failed to generate an image or the file does not exist.")
