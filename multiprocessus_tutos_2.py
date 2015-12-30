# Ici on crée deux workers, deux files d'attente et on 
# donne des taches différentes à chaque worker,
# par exemple toutes les taches 1 modulo 3 au worker 1 
# et les autres au worker 0. 
# Donc le worker 0 aura plus de travail que l'autre (stupide en soi).

# Attention à ne pas appliquer "get()" à une queue vide, cela bloque le script.
# pour cela, on peut regarder qsize() avant d'appliquer get().

import multiprocessing 
import time

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        # lancer les routines de la classe Process
        multiprocessing.Process.__init__(self)
        
        # comme les JoignableQueues sont des objets partagés,
        # il faut partager leurs références (voire leur contenu ?)
        # avec la mémoire de l'objet pour que celui-ci sache y 
        # accéder plus tard.
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        
        # la boucle while True maintient le processus actif ad vitam terminate-am :
        # la pillule de poison conduit à l'interruption
        
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print( '%s: Poison pill' % proc_name)
                self.task_queue.task_done()
                break
            # print( '%s: %s' % (proc_name, next_task)) 
            
            # c'est depuis ici que le script est lancé, par l'interprétation du *texte* 
            # passé par la file d'attente. 
            answer = next_task()
            
            # la fonction task_done est prédéfinie pour les JoignableQueues 
            self.task_queue.task_done()
            # mise sur la liste des choses faites
            self.result_queue.put(answer)
        return


class Produit(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self):
        time.sleep(0.1) # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)
    def __str__(self):
        return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
    # Establish communication queues
    num_consumers = 2 
    
    tasks = [ multiprocessing.JoinableQueue() for i in range(num_consumers) ]
    results = [ multiprocessing.Queue() for i in range(num_consumers) ]

    # Start consumers
    
    print( 'Creating %d consumers' % num_consumers)
    consumers = [ Consumer(tasks[i], results[i])
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    num_jobs = 20
    for j in range(num_jobs):
        tasks[j%3 == 1].put(Produit(j, j))
    
    # Add a poison pill for each consumer
    tasks[0].put(None)
    tasks[1].put(None)

    # Wait for all of the tasks to finish
    tasks[0].join()
    tasks[1].join()
    
    time.sleep(2)
    # Start printing results
    for i in range(num_consumers):
        while results[i].qsize():
            print('Le processus',str(i),'a calculé',results[i].get())
        
