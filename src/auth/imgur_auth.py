from imgurpython import ImgurClient

from util import *

def load_creds(file):
    auth = read_yml(file)

    return ImgurClient(auth["IMGUR_CLIENT_ID"], auth["IMGUR_CLIENT_SECRET"])