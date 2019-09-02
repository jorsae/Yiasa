""" Database TABLE NAMES """

TABLE_DOMAIN = 'domain'
TABLE_CRAWL_HISTORY = 'crawl_history'
TABLE_CRAWL_QUEUE = 'crawl_queue'
TABLE_EMAILS = 'emails'

def table_exists():
    return """SELECT name from sqlite_master WHERE type='table' and name=? """

def create_table_domain():
    return f"""CREATE TABLE {TABLE_DOMAIN} (
                scheme text,
                amount_crawled int,
                last_crawled date
    )"""

def create_table_crawl_history():
    return f"""CREATE TABLE {TABLE_CRAWL_HISTORY} (
                {TABLE_DOMAIN}_id int,
                url text,
                elapsed int,
                status_code int,
                crawled_date date,
                content_type text,
                content_length int,
                FOREIGN KEY ({TABLE_DOMAIN}_id) REFERENCES {TABLE_DOMAIN}(rowid)
    )"""

def create_table_crawl_queue():
    return f"""CREATE TABLE {TABLE_CRAWL_QUEUE} (
                domain text,
                priority int,
                date_added date
    )"""

def create_table_emails():
    return f"""CREATE TABLE {TABLE_EMAILS} (
                {TABLE_CRAWL_HISTORY}_id int,
                email text
                email_added date
    )"""