#!/usr/bin/env python3
import datetime
import sqlite3
from data_in import Import
# import mysql.connector as mysql


database = './db/downloads.db'


def drop_downloads_table(cur):
    cur.execute("DROP TABLE IF EXISTS downloads")


def create_downloads_table(cur):
    # TODO: why do i have to provide a primary key? this should be auto
    # TODO: is it worth putting more table columns in
    # TODO: data in as module and class
    # TODO: try blocks & errors

    # table requires:
    # magnet link
    # description
    # category
    # seeds
    # TODO: complete table links to manage downloads, metrics
    # priority
    # log of upgrade and downgrade
    # entryDate timestamp
    # downloadDate timestamp

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY,
                    magnet TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    seeds INTEGER,
                    priority TEXT,
                    entryDate timestamp,
                    downloadStart timestamp,
                    downloadDate timestamp
                    
                )
            """)


# def seed_table(cur, ts):

    # seed_data = [("magnetlink", "some download", "ebook", 5,
    #               f"{ts}", None), ("magnetlink2", "some download", "ebook", 5, f"{ts}", None)]
    # query = f'INSERT INTO downloads (magnet, description, category, seeds, downloadDate, downloadDate) VALUES (?,?,?,?,?,?)'

    # for row in seed_data:
    #     cur.execute(query, row)


def insert_download_data(cur, downloads, ts):

    query = f'INSERT INTO downloads (magnet, description, category, seeds, priority, entryDate, downloadStart, downloadDate) VALUES (?,?,?,?,?,?,?,?)'

    priority_interval = max([int(download["seeds"])
                            for download in downloads])/3

    def priority_sorter(seeds, priority_interval):
        if int(seeds) >= 2*priority_interval:
            return "H"
        elif int(seeds) <= priority_interval:
            return "L"
        else:
            return "M"

    for row in downloads:
        priority = priority_sorter(row["seeds"], priority_interval)
        insert_data = (row["href"], row["description"],
                       row["category"], row["seeds"], priority, f"{ts}", None, None)
        cur.execute(query, insert_data)
        print(insert_data)


def fetch_one(cur):
    cur.execute("SELECT * from downloads")
    return cur.fetchone()


def fetch_all(cur):
    cur.execute("SELECT * from downloads")
    return cur.fetchall()


def main():
    fin = r".\links.html"
    links_import = Import(raw_data_file=fin)
    downloads = links_import.getImportsData()

    db = sqlite3.connect(database=database)
    cur = db.cursor()

    # comment out if dont want to drop table
    drop_downloads_table(cur)
    db.commit()

    create_downloads_table(cur)
    db.commit()

    ts = datetime.datetime.now()
    # seed_table(cur, ts)
    # db.commit()

    insert_download_data(cur, downloads, ts)
    db.commit()

    # one_row = fetch_one(cur)
    # print(one_row)
    # all_rows = fetch_all(cur)
    # print(all_rows)

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
