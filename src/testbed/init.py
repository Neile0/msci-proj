from minicps.states import SQLiteState
from sqlite3 import OperationalError


PATH = "db.sqlite"
SCHEMA = "SCHEMA"


SCHEMA = """
CREATE TABLE pid_log (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""


# TODO Setup initial values
SCHEMA_INIT = """
    INSERT INTO swat_s1 VALUES ('FIT101',   1, '2.55');
    INSERT INTO swat_s1 VALUES ('MV101',    1, '0');
    INSERT INTO swat_s1 VALUES ('LIT101',   1, '0.500');
    INSERT INTO swat_s1 VALUES ('P101',     1, '1');

    INSERT INTO swat_s1 VALUES ('FIT201',   2, '2.45');
    INSERT INTO swat_s1 VALUES ('MV201',    2, '0');

    INSERT INTO swat_s1 VALUES ('LIT301',   3, '0.500');
"""



if __name__ == "__main__":

    try:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)
        print("{} successfully created.".format(PATH))
    except OperationalError:
        print("{} already exists.".format(PATH))