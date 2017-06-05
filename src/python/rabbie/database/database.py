import sqlite3
import datetime
import logging


logger = logging.getLogger(__name__)


class DataBase:

    def __init__(self, name: str) -> None:
        """
        Initialise data base object

        Parameters
        ----------
        name: str
            database name
        """
        if name.endswith('.db'):
            self.name = name
        else:
            self.name = '{}.db'.format(name)
        self.conn = sqlite3.connect(self.name)

        c = self.conn.cursor()
        c.execute('CREATE table IF NOT EXISTS measurements (timestamp DATETIME, name STRING, value INT, is_synced INT)')
        self.conn.commit()

        logger.debug('Connected to DB {}'.format(self.name))

    def insert_val(self, name: str, timestamp: datetime.datetime, value: int) -> None:
        """
        Insert measurement value into DB
        
        Parameters
        ----------
        timestamp: datetime.datetime
            UTC datetime when measurement was taken
        name: str  
            name to associate with value (non-unique)
        value: int
            value to log in DB
        """
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%SZ')
        c = self.conn.cursor()
        c.execute("INSERT INTO measurements VALUES (?, ?, ?, ?)",
                  (timestamp,       # timestamp
                   name,   # name
                   value,           # value
                   0))              # is_synced=False
        self.conn.commit()

        logger.info('Logged sensor reading ({}, {})'.format(timestamp, value))
