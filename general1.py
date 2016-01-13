# schéma de la structure du code

# imports
import math, random, numpy
import multiprocessing 
import time

# definir l'ouvrier
class Ouvrier(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, caract):
        # lancer les routines de la classe Process
        multiprocessing.Process.__init__(self)
        # files d'attentes personnelles
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.caract = caract

    def run(self):
        while True:
            # initialisation de quelques paramètres nécessaires à l'échelle Ouvrier
                #...
            
            # j'attends ce qui vient du chef            
            tache = task_queue.get() # bloque indéfiniment l'ouvrier
            commande = tache[0] # "task" (vient du chef) ou "call" (vient d'un autre ouvrier qui coopère)
            
            t = tache[1]        # indispensable ?
            
            
            if commande != "call":
                # si c'est une instance "originelle" (pas une sollicitation d'un ouvrier)
                # alors l'ouvrier choisit ce qu'il en fait
                choix = CLUPmax('''quels arguments''')
                
                if choix[0] == "call": 
                    # dans le cas où l'on fait appel à un autre
                    # on renvoie tout de suite le job à la queue de sortie
                    self.result_queue.put(choix)
                    
                    # augmenter les bons compteurs
                    
                    
                elif choix[0] == "bras":
                    # dans le cas où l'on a fait appel à l'un de ses propres bras
                    # j'ai un doute sur la différence entre les différents scripts CLUP x_x  :-( 
                    reward = CLUP(tache, choix[1], ...) 
                    # où choix[1] est le numéro du bras choisi
                    message = ["fini",tache,reward]
            
            # si qqn d'autre a fait appel à moi
            elif commande == "call":
                CLUP(...) # j'ai re un doute, désolé.
                
            elif commande == "finir":
                end()
                
            self.result_queue.put(message)
            self.task_queue.task_done() # je comprends un peu trop tard l'utilité de cette fonction :-/
            
    def end(self):
        # à la fin, faire remonter ses données.
        #...
    def CLUPcoop(arg1, arg2):
        # ...
    def CLUP(args...):
        # ...

# __main__ = script père
if __name__ == "__main__":
    
    # initialiser le père
    T = 1000
    nbWorkers = 4
    dimContexte = 2
    
    

    caractOuvriers = [ ['''compléter avec les spécialités de chaque ouvrier et de chaque bras'''] 
                        for i in range(nbWorkers) ]
    
    tasks = [ multiprocessing.JoinableQueue() for i in range(nbWorkers) ]
    results = [ multiprocessing.Queue() for i in range(nbWorkers) ]
    ouvriers = [ Ouvrier(tasks[i],results[i],caractOuvriers[i]) for i in range(nbWorkers) ]
    
    # générer les instances
    # Informations et contexte
    x_it = numpy.zeros((T,nbWorkers,dimContexte))
    for t in range(0,T):
        for m in range(0,nbWorkers):
            x_it[t,m,] = list(numpy.random.uniform(low=0.0, high=1.0,size=dimContexte)) # format liste
            
    
    # lancer les ouvriers :
    for o in ouvriers:
        o.start()
    
    # faire tourner le chronomètre
    for t in range(T):
        # envoyer les instances
        for i in range(nbWorkers):
            tasks[i].put(["task", t, x_it[t,i,]])
            
        # boucler jusqu'à avoir reçu nbWorkers fois "fini"
        while compteFinis < 4:
            # attendre les réponses : boucle tant que toutes les listes sont de longueur nulle
            # quand une liste a reçu qqch : laquelle ou lesquelles ? --> réactions
            for i in range(nbWorkers):
                if results[i].qsize() != 0:
                    resultat = results[i].get()
                    commande = resultat[0]
                    if commande == "fini":
                        compteFinis += 1
                    elif commande == "call":
                        destinataire = resultat['''mettre le bon index ici''']
                        tasks[destinataire].put(resultat)
        
        # quand on a reçu autant de "fini" qu'on avait envoyé de jobs,
        # ...
