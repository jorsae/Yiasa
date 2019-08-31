def create_table_fld():
    return """ CREATE TABLE FLD (
                scheme text,
                amount_crawled int,
                last_crawled date
    )"""

def create_table_crawl_history():
    return """CREATE TABLE crawl_history (
                fld.id int,
                url text,
                elapsed int,
                status_code int,
                crawled_date date,
                content_type text,
                content_length int,
                FOREIGN KEY (fld.id) REFERENCES FLD(rowid)
    )"""

def create_table_crawl_queue():
    return """ CREATE TABLE crawl_queue (
                fld text,
                priority int,
                date_added date
    )"""

def create_table_emails():
    return """ CREATE TABLE emails (
                crawl_history.id int,
                email text
                email_added date
    )"""