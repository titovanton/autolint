from pathlib import Path

import yaml

from .schemas import Config


def load_conf() -> Config:
    """
    Reads YAML file and parses by Config
    """

    # load default config
    module_path = Path(__file__).resolve()
    module_dir = module_path.parent
    def_conf_path = module_dir / 'config.yaml'

    with open(def_conf_path, 'r') as conf_file:
        conf_data = yaml.safe_load(conf_file)

    # load user local config
    local_conf = Path.home() / '.config/auto_lint/config.yaml'
    local_conf_data = {}

    if local_conf.exists():
        with open(local_conf, 'r') as conf_file:
            if data := yaml.safe_load(conf_file):
                local_conf_data = data

    conf_data |= local_conf_data
    conf = Config(**conf_data)
    return conf
