import pytest
import os

global fichierSrc
fichierSrc = "./ressources/input.txt"

def isEmptyFile(fichierSrc):
    if os.path.getsize(fichierSrc) == 0:
        return True
    return False

# vérifie si le fichier existe
def test_file_exist():
    assert os.path.isfile(fichierSrc) == True

# Vérifie si le fichier est vide
def test_no_empty_file():
    assert isEmptyFile(fichierSrc) == False

