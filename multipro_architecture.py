# procédure multiprocesseurs basique, avec partage de la mémoire entre processeurs 

from multiprocessing import Manager, Process
import random
random.seed(0)

def calcul(liste, ident, nombre):
    if isinstance(nombre,int):
        templiste = liste
        templiste[ident] += [nombre**2]
        liste = templiste
        #print('hey!')


if __name__ == '__main__':
    T=5
    manager = Manager()
    resultats = manager.list([ [] for proc in range(4)])
    
    taches = [[int(i/10),random.randint(0,15)] for i in range(0,40)]
    print('taches =',taches)
    
    # crée une séquence de tâches "adressées" à la mémoire d'un processeur particulier (i[0])
    pr = [Process(target=calcul, args=(resultats, i[0], i[1])) for i in taches]
    
    for each in pr:
        each.start()
    for each in pr:
        each.join()
    
    
    #pr = Process(target=calcul, args=(EtatsG, 0, 4))
    #calcul(resultats, 3, 12)
    #pr.start()
    #pr.join()
    print()
    print('resultats =',resultats)
