import re
import numpy as np
import logging

def lireFichier(cheminSource):
    fichierSource = open(cheminSource, 'r')
    global nbTondeuses, tondeuses, pelouse, nbCellsY
    nbTondeuses = 0
    tondeuses = []
    nbCellsY = int

    while True:
        # Nouvelle ligne depuis le fichier
        ligne = fichierSource.readline()
        refTondeuse = None
        if not ligne:
            break
        
        if re.search("\d.*\d$", ligne):
            # Taille de la pelouse
            nbCellsX = int(re.findall("\d+", ligne)[0]) + 1
            nbCellsY = int(re.findall("\d+", ligne)[1]) + 1
            pelouse = np.empty((nbCellsY,nbCellsX), list)
        
        # Position d'une tondeuse
        if re.search("\d.*\d.*(N|E|W|S)", ligne):
            nbTondeuses += 1
            x = int(re.findall("\d+", ligne)[0])
            y = int(re.findall("\d+", ligne)[1])
            orientationActuelle= ''.join(re.findall("\s+(N|S|E|O){1}\s+", ligne))
            infoTondeuse = []
            refTondeuse = "t" + str(nbTondeuses-1)
            infoTondeuse.append(refTondeuse)
            infoTondeuse.append(x)
            infoTondeuse.append(y)
            infoTondeuse.append(orientationActuelle)
            
            positionY = nbCellsY - 1 - y
            pelouse[positionY][x] = refTondeuse
            tondeuses.append(infoTondeuse)

        # Mouvements d'une tondeuse
        if re.search("^(A|D|G)+$", ligne):
            mouvements = re.findall("[A-G]{1}", ligne)        # [A-G]+
            indiceTondeuse = nbTondeuses-1
            tondeuses[indiceTondeuse].append(mouvements)
    fichierSource.close()


def afficherPelouse():  
    hauteurP = int(pelouse.shape[0])
    largeurP = int(pelouse.shape[1])
    for i in range(largeurP):
        print()
        for j in range(hauteurP):
            if pelouse[i][j]:
                print("T ", end='')
            else:
                print("* ", end='')
    print()

def obtenirNouvelleOrientation(orientationActuelle, prochainMouvement):
    if prochainMouvement != 'A':
        if prochainMouvement == 'D':
            if orientationActuelle == 'N':
                orientationActuelle = 'E'
            elif orientationActuelle == 'S':
                orientationActuelle = 'W'
            elif orientationActuelle == 'E':
                orientationActuelle = 'S'
            elif orientationActuelle == 'W':
                orientationActuelle = 'N'
        elif prochainMouvement == 'G':
            if orientationActuelle == 'N':
                orientationActuelle = 'W'
            elif orientationActuelle == 'S':
                orientationActuelle = 'E'
            elif orientationActuelle == 'E':
                orientationActuelle = 'N'
            elif orientationActuelle == 'W':
                orientationActuelle = 'S'            
    return orientationActuelle

def obtenirNouveauxCoordonnes(orientation, y, x):
    nouveauCoordY = y
    nouveauCoordX = x
    if orientation == 'S':
        nouveauCoordY = y - 1       # y+1 
    elif orientation == 'E':
        nouveauCoordX = x + 1
    elif orientation == 'N':
        nouveauCoordY = y + 1       # y-1
    elif orientation == 'W':
        nouveauCoordX = x - 1
    return nouveauCoordY, nouveauCoordX

def estAlInterieur(y=int, x=int):
    hauteurPelouse = pelouse.shape[0]
    largeurPelouse = pelouse.shape[1]
    if y < hauteurPelouse and y >= 0 and x < largeurPelouse and x >= 0:
        return True
    else:
        logging.warning("En dehors des limites : (%d, %d)", x, y)
        return False

def emplacementDispo(y, x):
    positionY = nbCellsY - 1 - y
    if pelouse[positionY][x]:
        logging.warning("Emplacement non disponible, %s est déjà présent", pelouse[positionY][x])
        return False
    return True        


def simulation():
    for i in range(nbTondeuses):
        infoTondeuse = tondeuses[i]
        refTondeuse = infoTondeuse[0]
        mouvements = infoTondeuse[4]
        prochainMouvement = mouvements[0]
        x = int
        y = int
        orientationActuelle = ''

        while prochainMouvement:
            x = infoTondeuse[1]
            y = infoTondeuse[2]          
            orientationActuelle = infoTondeuse[3]

            nouvelleOrientation = obtenirNouvelleOrientation(orientationActuelle,prochainMouvement)
            if nouvelleOrientation == orientationActuelle:
                nouveauCoordY, nouveauCoordX = obtenirNouveauxCoordonnes(orientationActuelle, y, x)
                # Vérifie si le mouvement est en dehors de la pelouse
                if estAlInterieur(nouveauCoordY, nouveauCoordX):        
                    # Vérfie si l'emplacement est disponible
                    if emplacementDispo(nouveauCoordY, nouveauCoordX):
                        # Libération de l'emplacement précédent
                        positionY = nbCellsY - 1 - y
                        pelouse[positionY][x] = None
                        # Intégration d'un nouvel emplacement
                        positionY = nbCellsY - 1 - nouveauCoordY
                        pelouse[positionY][nouveauCoordX] = refTondeuse
                        y = nouveauCoordY    
                        x = nouveauCoordX
            # Suppression du mouvement effectué
            mouvements = mouvements[1:]
            # Mise à jour des informations sur la tondeuse
            infoTondeuse = [refTondeuse, x, y, nouvelleOrientation, mouvements]
            if mouvements:
                prochainMouvement = mouvements[0]
            else:
                prochainMouvement = None
        tondeuses[i] = infoTondeuse
        print(x, y, orientationActuelle)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cheminSource = "./ressources/input.txt"
    lireFichier(cheminSource)
    #afficherPelouse()
    simulation()
    #afficherPelouse()
