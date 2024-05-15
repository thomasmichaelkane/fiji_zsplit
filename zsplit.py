import sys
import os
import numpy as np
import tifffile

def run():
    
    path = parse_args()
    
    zprojs = split_and_zproj(path)
    
    save_zprojs(zprojs, path)

################################################################

def split_and_zproj(path):
    
    stack = tifffile.imread(path)

    log = f"Number of images: {stack.shape[0]} | Number of frames to average: {stack.shape[1]}"
    print(log)

    zprojs = np.mean(stack, 1)

    return zprojs

def save_zprojs(zprojs, path):
    
    folder, orig_name = os.path.split(path)
    basename, _ = os.path.splitext(orig_name)
    zproj_name = basename +  "_Z-projections.tif"
    zproj_path = os.path.join(folder, zproj_name)
    tifffile.imwrite(zproj_path, zprojs)

def parse_tiff(arg):

    if os.path.exists(arg):
        
        if arg.endswith('.tiff') or arg.endswith('.tif'):
            return arg
        
        else:
            raise FileNotFoundError("The file is not a tiff")
            
    else:
        raise FileNotFoundError

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No tiff specified")
        
    if len(sys.argv) == 2:
        
        path = parse_tiff(sys.argv[1])

    if len(sys.argv) >= 3:

        raise KeyError("Too many arguments")
        
    return path

if __name__ == "__main__":
    
    run()

    
