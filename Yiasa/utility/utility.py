import logging
import globvar
import os

def setup_logging():
    """ Sets up logging """
    # Creates log folder
    if not os.path.isdir(globvar.log_folder):
        os.makedirs(globvar.log_folder)

    logging.basicConfig(filename=f'{globvar.log_folder}/{globvar.log_file}', level=logging.DEBUG, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

def get_fld(url):
    """ gets first level domain from a url """
    return url.split("//")[-1].split("/")[0].split('?')[0]

def same_fld(fld1, fld2):
    fld1 = fld1.replace('www.', '')
    fld2 = fld2.replace('www.', '')
    return fld1 == fld2