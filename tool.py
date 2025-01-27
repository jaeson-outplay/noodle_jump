from smolagents import Tool

class FileUpdateTool(Tool):
    name = "file_update_tool"
    description ="""
    this tool will be used to update the file in a given directory with the provided new file directory.
    """
    inputs = {
        "target_file_location": {
            "type": "string",
            "description": "the location of the file that will be replaced"
        },
        "new_file_location": {
            "type": "string",
            "description": "the location of the new file to replace target file location"
        }
    }
    output_type = "string"
    def forward(self, target_file_location, new_file_location) -> str:
        import os
        import shutil

        if os.path.exists(new_file_location):
            # Define the destination path for the saved image
        #     # Create the './generatedImages' directory if it doesn't exist
        #     # Copy the image from the temporary location to the desired directory
            shutil.copy(new_file_location, target_file_location)

            return print(f"Image saved to {target_file_location}")
        else:
            return print("Failed to generate an image or the file does not exist.")
        

class GitPushTool(Tool):
    name = "git_push_tool"
    description = """
    This tool will be triggered to create a new branch and push new changes to the repository.
    """
    inputs = {
        "branch_name": {
            "type": "string",
            "description": "the target branch that will be pushed, new or existing."
        }
    }
    output_type = "string"

    def forward(self, branch_name) -> str:
        import os
        import subprocess
        try:
            gitUsername = os.getenv("GIT_USERNAME")
            gitEmail = os.getenv("GIT_EMAIL")
            # new_branch = "add-generated-image-2"
            # Step 1: Ensure we are in a Git repository
            subprocess.run(["git", "status"], check=True)

            # Step 2: Create and switch to a new branch
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            print(f"Checked out to new branch: {branch_name}")

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
            subprocess.run(["git", "push", "--set-upstream", "origin", branch_name], check=True)
            return print(f"Branch '{branch_name}' pushed to remote repository.")
        except subprocess.CalledProcessError as e:
            return print(f"An error occurred while performing Git operations: {e}")

class FindFilesTool(Tool):
    name = "find_files"
    description = "Find files with a given extension in a directory and its subdirectories"
    inputs = {"extension":{"type":"string","description":"the place from which you start your ride"}}
  
    output_type = "string"

    def forward(self, extension: str) -> str:
        """
        Recursively search for files with a given extension in a directory and its subdirectories.

        Args:
            extension: The file extension to look for (e.g., '.txt')
        """
        import os

        root_dir = "./"
        found_files = []

        # Walk through the directory tree
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(extension):
                    filepath = os.path.join(dirpath, filename)
                    absolute_path = os.path.abspath(filepath)
                    found_files.append(absolute_path)

        return found_files