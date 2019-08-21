import logging
import globvar

def setup_logging():
    """ Sets up logging """
    logging.basicConfig(filename=f'{globvar.log_folder}/{globvar.log_file}', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s %(message)s')

def get_fld(url):
    """ gets first level domain from a url """
    return url.split("//")[-1].split("/")[0].split('?')[0]