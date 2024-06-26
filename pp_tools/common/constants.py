import os

env_var = os.environ
if 'BASE_PATH' not in env_var:
    CURRENT_PATH = os.path.abspath(__file__)
    COMMON_PATH = os.path.dirname(CURRENT_PATH)
    PP_TOOLS_PATH = os.path.dirname(COMMON_PATH)
    BASE_PATH = PP_TOOLS_PATH
LOCAL_DATA_PATH = os.path.join(BASE_PATH, 'LOCAL_DATA')
CONFIG_PATH = os.path.join(LOCAL_DATA_PATH, 'LOCAL_CONFIGS')
DATA_OUTPUT_PATH = os.path.join(LOCAL_DATA_PATH, 'DATA')
LOGS_PATH = os.path.join(LOCAL_DATA_PATH, 'LOGS')
TEST_DATA_OUTPUT_PATH = os.path.join(LOCAL_DATA_PATH, 'TEST_DATA')
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, 'config.yml')
PATH_STRUCTURE = [
    {
        "path": LOCAL_DATA_PATH,
        "children": [
            {
                "path": CONFIG_PATH,
                "children": []
            }, 
            {
                "path": DATA_OUTPUT_PATH,
                "children": []
            },
            {
                "path": LOGS_PATH,
                "children": []
            },
            {
                "path": TEST_DATA_OUTPUT_PATH,
                "children": []
            },
        ]
    }
]
# Constant Variables used by package
APP_NAME = 'pp_tools'
DEFAULT_LOG_LEVEL = 'INFO'



if __name__ == '__main__':
    print(CURRENT_PATH)
    print(COMMON_PATH)
    print(PP_TOOLS_PATH)