import sqlite3

conn = sqlite3.connect("db.sqlite3")

# try initialize database structure
cur = conn.cursor()
# resp = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
# print(resp.fetchall())
# cur.execute("drop table antispam_keyword")
cur.execute(
    """create table if not exists antispam_keyword (
    id integer primary key,
    keyword text not null,
    score integer not null,
    created_time integer not null,
    modified_time integer not null
)"""
)
cur.execute(
    """create index if not exists antispam_keyword_idx_created_time on antispam_keyword(
    created_time
)"""
)
cur.execute(
    """create index if not exists antispam_keyword_idx_modified_time on antispam_keyword(
    modified_time
)"""
)
cur.execute(
    """create index if not exists antispam_keyword_idx_keyword on antispam_keyword(
    keyword
)"""
)
conn.commit()


def getConn():
    return conn
