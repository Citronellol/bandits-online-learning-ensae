# Code commenté pour cet exemple : https://pymotw.com/2/multiprocessing/communication.html#passing-messages-to-processes 

# Attention, dans cet exemple, les Queues ne sont pas nominales.
# Il est impossible de demander à tel worker (Consumer) de faire le travail,
# il n'y a qu'une seule file d'attente qui fonctionne plus ou moins par attribution
# successive en fonction de l'ancienneté des workers.

# Comme nous avons besoin de pouvoir attribuer un job à un worker particulier (sur 4), 
# nous allons devoir créer quatre files d'attente (à venir).

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
                print( '%s: Poison pill \r' % proc_name)
                self.task_queue.task_done()
                break
            print( '%s: %s' % (proc_name, next_task)) 
            
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
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print( 'Creating %d consumers' % num_consumers)
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    num_jobs = 20
    for i in range(num_jobs):
        tasks.put(Produit(i, i))
    
    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    
    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1
        
time.sleep(2)
