from smolagents import Tool

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
                    found_files.append(filepath)

        return found_files