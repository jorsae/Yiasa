""" Database TABLE NAMES """

TABLE_DOMAIN = 'domain'
TABLE_CRAWL_HISTORY = 'crawl_history'
TABLE_CRAWL_QUEUE = 'crawl_queue'
TABLE_EMAILS = 'emails'

table_exists = """SELECT name from sqlite_master WHERE type='table' and name=? """

insert_table_domain = f'INSERT INTO {TABLE_DOMAIN} VALUES (?, ?, ?)'

create_table_domain = f"""CREATE TABLE {TABLE_DOMAIN} (
                scheme text,
                amount_crawled int,
                last_crawled date
    )"""

create_table_crawl_history = f"""CREATE TABLE {TABLE_CRAWL_HISTORY} (
                {TABLE_DOMAIN}_id int,
                url text,
                elapsed int,
                status_code int,
                crawled_date date,
                content_type text,
                content_length int,
                FOREIGN KEY ({TABLE_DOMAIN}_id) REFERENCES {TABLE_DOMAIN}(rowid)
    )"""

create_table_crawl_queue = f"""CREATE TABLE {TABLE_CRAWL_QUEUE} (
                domain text,
                priority int,
                date_added date
    )"""

create_table_emails = f"""CREATE TABLE {TABLE_EMAILS} (
                {TABLE_CRAWL_HISTORY}_id int,
                email text
                email_added date
    )"""