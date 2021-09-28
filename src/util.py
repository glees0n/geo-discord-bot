import yaml

def loadYML(file):
    with open(file) as file:
            auth = yaml.load(file, Loader=yaml.FullLoader)
    
    return auth