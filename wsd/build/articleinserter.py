import Queue
import threading
import multiprocessing

MAX_WAIT_QUEUE_TIMEOUT = 2

#class ArticleInserter(threading.Thread):
class ArticleInserter(threading.Thread):
    '''Thread which inserts articles into the database
    '''

    def __init__(self, queue, build_view):
        threading.Thread.__init__(self)
        '''constructor

           @param queue the queue to which the articles and redirects are read
           @param build_view the database build view to use to connect to the database
        '''

        self._queue = queue
        self._build_view = build_view
        self._end = False

    def run(self):
        while not self._end:
            try:
                # fetch item from queue
                item = self._queue.get(True, MAX_WAIT_QUEUE_TIMEOUT)

                # insert as article or redirect respectively
                if item['type'] == 'article':
                    self._build_view.insert_article(item['id'], item['rev_id'], item['title'])
                else:
                    self._build_view.insert_redirect(item['title'], item['target'])

                # commit and mark as done
                self._build_view.commit()
                self._build_view.reset_cache()
                self._queue.task_done()
            except Queue.Empty:
                pass

    def end(self):
        self._end = True


