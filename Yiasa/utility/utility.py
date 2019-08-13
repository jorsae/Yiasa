def get_fld(url):
    """ gets first level domain from a url """
    return url.split("//")[-1].split("/")[0].split('?')[0]