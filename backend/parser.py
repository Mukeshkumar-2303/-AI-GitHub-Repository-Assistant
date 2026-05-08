import os


# CONFIG

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".java",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".sql",
    ".html",
    ".css"
]

IGNORE_FOLDERS = [
    "node_modules",
    ".git",
    "__pycache__",
    "build",
    "dist",
    ".next",
    "venv",
    "repositories"
]



# LOAD FILES (FOR RAG)

def load_repository_files(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):

        # ignore unwanted folders
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_FOLDERS
        ]

        for file in files:

            ext = os.path.splitext(file)[1]

            if ext in SUPPORTED_EXTENSIONS:

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    documents.append({
                        "file_path": file_path,
                        "content": content
                    })

                except Exception:
                    # skip unreadable files safely
                    pass

    return documents



# FILE STRUCTURE

def get_file_structure(repo_path):
    """
    Returns ONLY real file paths from repository.
    Used to prevent LLM hallucination.
    """

    file_list = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_FOLDERS
        ]

        for file in files:

            ext = os.path.splitext(file)[1]

            if ext in SUPPORTED_EXTENSIONS:

                full_path = os.path.join(root, file)
                file_list.append(full_path)

    return file_list
