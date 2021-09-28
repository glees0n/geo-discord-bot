from imgurpython import ImgurClient

from util import *

def loadCreds(file):
    auth = loadYML(file)

    return ImgurClient(auth["IMGUR_CLIENT_ID"], auth["IMGUR_CLIENT_SECRET"])