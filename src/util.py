import yaml

def read_yml(file):
    with open(file) as file:
            auth = yaml.load(file, Loader=yaml.FullLoader)
    
    return auth