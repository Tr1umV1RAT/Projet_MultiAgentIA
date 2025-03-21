class FileManager:
    def sauvegarder(self, fichier, contenu):
        with open(fichier, "w") as f:
            f.write(contenu)
