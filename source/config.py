import yaml

def load_config():
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

CONFIG = load_config()
