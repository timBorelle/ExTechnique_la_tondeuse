import re
import numpy as np
import logging


def lireFichier(cheminSource):
    logging.info("lireFichier")
    fichierSource = open(cheminSource, 'r')
    global nbTondeuses, tondeuses, pelouse, nbCellsY
    nbTondeuses = 0
    tondeuses = []
    nbCellsY = int

    while True:
        # Nouvelle ligne depuis le fichier
        ligne = fichierSource.readline()
        refTondeuse = None
        #logging.info(ligne)
        if not ligne:
            break
        
        if re.search("\d.*\d$", ligne):
            # Taille de la pelouse
            nbCellsX = int(re.findall("\d+", ligne)[0]) + 1
            nbCellsY = int(re.findall("\d+", ligne)[1]) + 1
            pelouse = np.empty((nbCellsY,nbCellsX), list)
            logging.info("Taille de la pelouse: (%d, %d)", nbCellsX, nbCellsY)
        
        # Position d'une tondeuse
        if re.search("\d.*\d.*(N|E|W|S)", ligne):
            nbTondeuses += 1
            x = int(re.findall("\d+", ligne)[0])
            y = int(re.findall("\d+", ligne)[1])
            #orientationActuelle= re.findall("\s+(N|S|E|O){1}\s+", ligne)
            #orientationActuelle= re.findall("(N|E|W|S)+", ligne)
            orientationActuelle= ''.join(re.findall("\s+(N|S|E|O){1}\s+", ligne))
            logging.info("orientationActuelle: %s", str(orientationActuelle))
            infoTondeuse = []
            refTondeuse = "t" + str(nbTondeuses-1)
            infoTondeuse.append(refTondeuse)
            infoTondeuse.append(x)
            infoTondeuse.append(y)
            infoTondeuse.append(orientationActuelle)
            logging.info("nouvelle tondeuse: %s", str(infoTondeuse))
            
            positionY = nbCellsY - 1 - y
            pelouse[positionY][x] = refTondeuse
            logging.info("tondeuse #%s", pelouse[positionY][x])
            tondeuses.append(infoTondeuse)
            logging.info("tondeuses : %s", str(tondeuses))

        # Mouvements d'une tondeuse
        if re.search("^(A|D|G)+$", ligne):
            mouvements = re.findall("[A-G]{1}", ligne)        # [A-G]+
            logging.info("Mouvements: %s", str(mouvements))
            #logging.info("tondeuse iNfO + mouv : ")
            indiceTondeuse = nbTondeuses-1
            tondeuses[indiceTondeuse].append(mouvements)
            #tondeuses.insert(nbTondeuses-1, mouvements)
            #logging.info(tondeuses)
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
    hauteurPelouse = pelouse.shape[0] + 1
    largeurPelouse = pelouse.shape[1] + 1
    if y < hauteurPelouse and y >= 0 and x < largeurPelouse and x >= 0:
        return True
    else:
        logging.error("En dehors des limites : (%d, %d)", x, y)
        return False

def emplacementDispo(y, x):
    positionY = nbCellsY - 1 - y
    if pelouse[positionY][x]:
        #logging.info("pelouse[y][x] : %s", pelouse[y][x])
        #logging.warning("Emplacement non disponible.")
        return False
    return True        


def simulation():
    logging.info("Simulation...")
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
            y = infoTondeuse[2]     #nbCellsY - 1 - infoTondeuse[2]      
            orientationActuelle = infoTondeuse[3]
        
            #print("prochain mouv ###")
            #print(prochainMouvement)
            #logging.info("orientationActuelle : {%s}", orientationActuelle)
            nouvelleOrientation = obtenirNouvelleOrientation(orientationActuelle,prochainMouvement)
            #logging.info("nouvelleOrientation : {%s}", str(nouvelleOrientation))
            '''if nouvelleOrientation != orientationActuelle:
                print(end="")
                #mouvements = mouvements[1:]
                # Mise à jour des informations sur la tondeuse
                #tondeuses[i] = [refTondeuse, x, y, nouvelleOrientation, mouvements]
            else:'''
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
                y = nouveauCoordY    #positionY
                x = nouveauCoordX
            # Suppression du mouvement effectué
            mouvements = mouvements[1:]
            # Mise à jour des informations sur la tondeuse
            infoTondeuse = [refTondeuse, x, y, nouvelleOrientation, mouvements]
            #tondeuses[i] = [refTondeuse, x, y, nouvelleOrientation, mouvements]
            if mouvements:
                prochainMouvement = mouvements[0]
            else:
                prochainMouvement = None
            #logging.info("infoTondeuse : ")
            logging.info(infoTondeuse)
        tondeuses[i] = infoTondeuse
        logging.info("----- %s a effectué tous ses mouvements. -----", refTondeuse)
        print(x, y, orientationActuelle)
        

    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cheminSource = "./ressources/input.txt"
    lireFichier(cheminSource)
    afficherPelouse()
    simulation()
    logging.info("nouvelle pelouse :")
    afficherPelouse()
    print(tondeuses)
