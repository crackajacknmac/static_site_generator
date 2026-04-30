import os
import shutil

def generator(static, public):
    if not os.path.exists(public):
        os.mkdir(public)
    
    static_list = os.listdir(static)
    for name in static_list:
        static_file_path = os.path.join(static, name)
        public_file_path = os.path.join(public, name)

        if os.path.isfile(static_file_path):
            shutil.copy(static_file_path, public_file_path)
        if os.path.isdir(static_file_path):
            os.mkdir(public_file_path)
            generator(static_file_path, public_file_path)




