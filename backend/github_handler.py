import os
# 🚨 Prevent ANY git credential popup (Windows fix)
os.environ["GIT_TERMINAL_PROMPT"] = "0"
os.environ["GCM_INTERACTIVE"] = "never"

import re
import shutil
import uuid
import time
import requests
from git import Repo


# CONFIG

REPO_DIR = "repositories"



# Validate GitHub URL

def validate_github_url(url):
    pattern = r"^https://github\.com/[\w.-]+/[\w.-]+/?$"

    if not url:
        return False

    if not re.match(pattern, url):
        return False

    if " " in url or "github.com/" not in url:
        return False

    return True



#  FAST REPO CHECK (IMPORTANT FIX)
# -----------------------------
def check_repo_exists(repo_url):
    try:
        parts = repo_url.replace("https://github.com/", "").strip("/").split("/")

        if len(parts) != 2:
            return False

        owner, repo = parts[0], parts[1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        response = requests.get(api_url, timeout=5)

        return response.status_code == 200

    except Exception:
        return False



# SAFE DELETE 

def safe_remove(path):
    if os.path.exists(path):
        for _ in range(3):
            try:
                shutil.rmtree(path, ignore_errors=False)
                return
            except Exception:
                time.sleep(1)

        shutil.rmtree(path, ignore_errors=True)



# MAIN CLONE FUNCTION

def clone_repository(repo_url):
    try:

       
        if not validate_github_url(repo_url):
            return None, "❌ Invalid GitHub repository URL."

     
        if not check_repo_exists(repo_url):
            return None, "❌ Repository does not exist or is private."

        
        os.makedirs(REPO_DIR, exist_ok=True)

      
        repo_id = str(uuid.uuid4())
        local_path = os.path.join(REPO_DIR, repo_id)

      
        safe_remove(local_path)

        Repo.clone_from(repo_url, local_path)

        return local_path, None

    except Exception as e:
        return None, f"❌ Clone Error: {str(e)}"
