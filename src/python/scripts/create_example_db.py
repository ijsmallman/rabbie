from rabbie.database import DataBase
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Simple script to make a database of fake values')
    parser.add_argument('name', type=str, help="Name for database")
    parser.add_argument('-n', type=int, default=1000, help="Number of entries")
    args = parser.parse_args()

    db = DataBase(args.name)

    t0 = datetime.utcnow()
    for i in range(args.n):
        db.insert_val('sample',
                      t0+timedelta(0, 0, 0, 0, i*15),
                      int(255*(np.sin(2*i*np.pi/100)+1)/2))

    logging.info('{} entries inserted into DB'.format(args.n))
