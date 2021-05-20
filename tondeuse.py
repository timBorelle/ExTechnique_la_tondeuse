import re
#from types import DynamicClassAttribute
import numpy as np
import logging

global nbTondeuses, tondeuses



def lireFichier(cheminSource):
    logging.info("lireFichier")
    fichierSource = open(cheminSource, 'r')
    global pelouse
    nbTondeuses = 0
    tondeuses = []

    while True:
        # Nouvelle ligne depuis le fichier
        ligne = fichierSource.readline()
        refTondeuse = None
        #logging.info(ligne)
        if not ligne:
            logging.warning("break!")
            break
        
        if re.search("\d.*\d$", ligne):
            # Taille de la pelouse
            nbCellsX = int(re.findall("\d+", ligne)[0])
            nbCellsY = int(re.findall("\d+", ligne)[1])
            pelouse = np.empty((nbCellsY,nbCellsX), list)
            logging.info("Taille de la pelouse: (%d, %d)", nbCellsX, nbCellsY)
        
        # Position d'une tondeuse
        if re.search("\d.*\d.*(N|E|W|S)", ligne):
            nbTondeuses += 1
            x = int(re.findall("\d+", ligne)[0])
            y = int(re.findall("\d+", ligne)[1])
            orientation = re.findall("\s+(N|S|E|O){1}\s+", ligne)
            logging.info("Orientation : %s", str(orientation))
            infoTondeuse = []
            refTondeuse = "t" + str(nbTondeuses-1)
            infoTondeuse.append(refTondeuse)
            infoTondeuse.append(x)
            infoTondeuse.append(y)
            infoTondeuse.append(orientation)
            logging.info("nouvelle tondeuse: %s", str(infoTondeuse))
            
            pelouse[y][x] = refTondeuse
            logging.info("tondeuse #%s", pelouse[y][x])
            tondeuses.append(infoTondeuse)
            logging.info("tondeuses : %s", str(tondeuses))

        # Mouvements d'une tondeuse
        if re.search("^(A|D|G)+$", ligne):
            mouvements = re.findall("[A-G]+", ligne)        # [A-G]{1}
            logging.info("Mouvements: %s", str(mouvements))
            logging.info("tondeuse iNfO + mouv : ")
            indiceTondeuse = nbTondeuses-1
            tondeuses[indiceTondeuse].append(mouvements)
            #tondeuses.insert(nbTondeuses-1, mouvements)
            logging.info(tondeuses)
            #logging.info("tondeuses.pop : ")
            #logging.info(tondeuses.pop())
            
    
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cheminSource = "./ressources/input.txt"
    lireFichier(cheminSource)
    afficherPelouse()
