import warnings
from osconfeed_19_2 import load

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def load_db(db):
    raw_data = load()
    warnings.warn('loading' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = Record(**record)


def test():
    import shelve
    db = shelve.open(DB_NAME)
    if CONFERENCE not in db:
        load_db(db)

    speaker = db['speaker.3471']
    print(type(speaker))
    print(speaker.name, speaker.twitter)
    db.close()


if __name__ == "__main__":
    test()




