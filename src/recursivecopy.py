import os
import shutil

def copy_tree(src, dst, delete_dst=True):
    #if delete_dst and os.path.exists(dst):
    #    shutil.rmtree(dst)
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_tree(s, d)
        else:
            shutil.copy2(s, d)
