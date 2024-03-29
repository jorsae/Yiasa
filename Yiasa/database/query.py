# Database TABLE NAMES
TABLE_DOMAIN = 'domain'
TABLE_CRAWL_QUEUE = 'crawl_queue'
TABLE_CRAWL_HISTORY = 'crawl_history'
TABLE_EMAILS = 'emails'

# General queries
table_exists = """SELECT name from sqlite_master WHERE type='table' and name=? """

get_id_domain = f'SELECT rowid from {TABLE_DOMAIN} where FLD = ?'

# Insert queries
insert_table_domain = f'INSERT INTO {TABLE_DOMAIN} VALUES (?, ?, ?, ?, ?)'
insert_table_crawl_queue = f'INSERT INTO {TABLE_CRAWL_QUEUE} VALUES (?, ?, ?)'
insert_table_crawl_history = f'INSERT INTO {TABLE_CRAWL_HISTORY} VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
insert_table_emails = f'INSERT INTO {TABLE_EMAILS} VALUES (?, ?, ?)'
insert_table_emails_with_fld = f"""INSERT INTO {TABLE_EMAILS}
                                    VALUES ((SELECT rowid FROM {TABLE_DOMAIN} WHERE FLD = ?), ?, ?)"""

# Update queries
update_table_domain = f'UPDATE {TABLE_DOMAIN} SET amount_crawled = amount_crawled + 1, last_crawled = ? WHERE rowid = ?'

# Create queries
create_table_domain = f"""CREATE TABLE {TABLE_DOMAIN} (
                scheme text,
                FLD text,
                amount_crawled int,
                first_crawled date,
                last_crawled date,
                PRIMARY KEY(FLD)
    )"""

create_table_crawl_history = f"""CREATE TABLE {TABLE_CRAWL_HISTORY} (
                {TABLE_DOMAIN}_id int,
                url text,
                elapsed int,
                status_code int,
                crawled_date date,
                content_type text,
                content_length int,
                new_location text,
                FOREIGN KEY ({TABLE_DOMAIN}_id) REFERENCES {TABLE_DOMAIN}(rowid)
    )"""

create_table_crawl_queue = f"""CREATE TABLE {TABLE_CRAWL_QUEUE} (
                domain text,
                priority int,
                date_added date,
                PRIMARY KEY(domain)
    )"""

create_table_emails = f"""CREATE TABLE {TABLE_EMAILS} (
                {TABLE_DOMAIN}_id int,
                email text,
                email_added date,
                FOREIGN KEY ({TABLE_DOMAIN}_id) REFERENCES {TABLE_DOMAIN}(rowid)
    )"""