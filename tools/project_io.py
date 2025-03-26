import os
import json
import shutil

class ProjectIO:
    @staticmethod
    def save_project(project_data, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=4)

    @staticmethod
    def load_project(filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def ensure_dir(directory):
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def delete_file(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def copy_file(src, dst):
        shutil.copy2(src, dst)

    @staticmethod
    def move_file(src, dst):
        shutil.move(src, dst)

    @staticmethod
    def list_files(directory, extension=None):
        files = []
        for filename in os.listdir(directory):
            if extension is None or filename.endswith(extension):
                files.append(filename)
        return files
