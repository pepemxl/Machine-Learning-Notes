import os
import yaml
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.constants import CONFIG_FILE_PATH


if __name__ == '__main__':
    print(CONFIG_FILE_PATH)
