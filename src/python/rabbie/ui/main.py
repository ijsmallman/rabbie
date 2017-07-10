if __name__ == '__main__':
    from rabbie.database import DataBase
    from threading import Thread
    import time


    def add_entries(q):

        db = DataBase('../../scripts/example.db')
        entries = db.fetch_entries()
        n = len(entries)
        for i in range(1, n):
            q.put(entries[:i])
            time.sleep(2)


    q = Queue()

    t = Thread(target=add_entries, args=(q,))
    t.daemon = True
    t.start()

    lp = LivePlot(q)
    lp.show()
