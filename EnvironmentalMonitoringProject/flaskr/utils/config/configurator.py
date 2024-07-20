import yaml
import os
import sys
from yaml import FullLoader

yaml_filename = 'confs/app_config.yaml'


def read_yaml_conf(logger):
    try:
        with open(yaml_filename, 'r') as file:
            result = yaml.load(file, Loader=FullLoader)
    except FileNotFoundError:
        logger.warning('<' + os.path.basename(__file__) + '>' + " - " + yaml_filename + " file not founded....\n")
        logger.error('<' + os.path.basename(__file__) + '>' + " - terminating application...\n")
        # exit python process
        sys.exit()
    logger.info('<' + os.path.basename(__file__) + '>' + " - Yaml reading is OK....\n")
    return result
