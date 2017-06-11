import sqlite3
import datetime
import logging
from typing import List

logger = logging.getLogger(__name__)


TABLE_NAME = "readings"


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
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = dict_factory

        query = 'CREATE table IF NOT EXISTS ' + \
                TABLE_NAME + ' ' \
                '([measured-at] TIMESTAMP, name STRING, value INT, [is-synced] INT)'

        c = self.conn.cursor()
        c.execute(query)
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
            
        Notes
        -----
        sqlite3 has a bug that results in an error during fetch if timestamp has a timezone. 
        """
        query = "INSERT INTO " + \
                TABLE_NAME + " " + \
                "VALUES (?, ?, ?, ?)"
        c = self.conn.cursor()
        c.execute(query,
                  (timestamp,       # timestamp
                   name,            # name
                   value,           # value
                   0))              # is-synced=False
        self.conn.commit()

        logger.info('Logged sensor reading ({}, {})'.format(timestamp, value))

    def entry_count(self, name: str) -> int:
        """
        Count database entries with given name
        
        Parameters
        ----------
        name: str
            entry name to count

        Returns
        -------
        counts: int
            number of entries with name in database
        """
        query = "SELECT COUNT(*) from " + \
                TABLE_NAME + " " + \
                "WHERE name=?"
        c = self.conn.cursor()
        rows = c.execute(query, (name,)).fetchone()['COUNT(*)']
        return rows

    def fetch_entries(self,
                      from_datetime: datetime.datetime=None,
                      to_datetime: datetime.datetime=None,
                      filter_synced: bool=False) -> List[dict]:
        """
        Fetch entries from database
        
        Parameters
        ----------
        from_datetime: datetime.datetime
            start timestamp (default: None)
        to_datetime: datetime.datetime
            end timestamp (default: None)
        filter_synced: bool
            filter out all synced data (default: False)

        Returns
        -------
        entries: List[dict]
            database entries
        """
        c = self.conn.cursor()

        if (from_datetime is None) and (to_datetime is None):
            if filter_synced:
                c.execute("SELECT * FROM " +
                          TABLE_NAME + " " +
                          "WHERE [is-synced] = ?", (0,))
            else:
                c.execute("SELECT * FROM " + TABLE_NAME)

        elif from_datetime is None:
            if filter_synced:
                c.execute('SELECT * FROM ' +
                          TABLE_NAME + ' ' +
                          'WHERE timestamp <= ? ' +
                          'AND [is-synced] = ?', (to_datetime, 0))
            else:
                c.execute('SELECT * FROM ' +
                          TABLE_NAME + ' ' +
                          'WHERE [measured-at] <= ?', (to_datetime,))

        elif to_datetime is None:
            if filter_synced:
                c.execute('SELECT * FROM ' +
                          TABLE_NAME + ' ' +
                          'WHERE [measured-at] >= ? ' +
                          'AND [is-synced] = ?', (from_datetime, 0))
            else:
                c.execute('SELECT * FROM ' +
                          TABLE_NAME + ' ' +
                          'WHERE [measured-at] >= ?', (from_datetime,))
        else:
            if filter_synced:
                c.execute('SELECT * FROM ' +
                          TABLE_NAME + ' ' +
                          'WHERE [is-synced] = ? ' +
                          'AND [measured-at] BETWEEN ? AND ?', (0, from_datetime, to_datetime))
            else:
                c.execute('SELECT * FROM ' +
                          TABLE_NAME + ' ' +
                          'WHERE [measured-at] BETWEEN ? AND ?', (from_datetime, to_datetime))

        entries = c.fetchall()
        return entries

    def fetch_entry(self, timestamp: datetime) -> dict:
        """
        Fetch single entry from database by timestamp
        
        Parameters
        ----------
        timestamp: datetime.datetime
            timestamp for database entry

        Returns
        -------
        entry: dict
            the database entry
        """
        c = self.conn.cursor()
        c.execute('SELECT * FROM ' +
                  TABLE_NAME + ' ' +
                  'WHERE [measured-at] = ?',
                  (timestamp,))
        entry = c.fetchone()
        return entry

    def update_sync_status(self,
                           timestamp: datetime.datetime,
                           status: bool) -> None:
        c = self.conn.cursor()
        c.execute('UPDATE ' + TABLE_NAME + ' SET ' +
                  '[is-synced] = ? WHERE [measured-at] = ?',
                  (int(status), timestamp))
        self.conn.commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        if col[0] == 'is-synced':
            d[col[0]] = (True if row[idx] == 1 else False)
        else:
            d[col[0]] = row[idx]
    return d
