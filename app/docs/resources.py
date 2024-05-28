

import os


# Static function for getting relative paths
def base_path(relative_path):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_script_dir))
    path = os.path.join(base_dir, f'app/docs/{relative_path}')
    # print(path)
    return path