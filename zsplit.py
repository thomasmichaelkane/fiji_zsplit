import sys
import os
import numpy as np
import tifffile

def run():
    
    path, frames_per_acq = parse_args()
    
    stack, total_frames = read_stack(path, frames_per_acq)
    
    zprojs = split_and_zproj(stack, frames_per_acq, total_frames)
    
    save_zprojs(zprojs, path)

################################################################

def read_stack(path, frames_per_acq):

    tiff_stack = tifffile.imread(path)

    total_frames = tiff_stack.shape[0]

    if total_frames % frames_per_acq != 0:
        raise ValueError("The total frame number of the stack but be divisible by the frames per acqisition")
    else:
        num_new_stacks = int(total_frames / frames_per_acq)
        log = f"Splitting {total_frames} frames length tiff stack into {num_new_stacks} Z-projections, with {frames_per_acq} frames per projection"
        print(log)
        
    return tiff_stack, total_frames

def split_and_zproj(tiff_stack, frames_per_acq, total_frames):
    
    acqs = [tiff_stack[i:i+frames_per_acq, :, :] for i in range(0, total_frames, frames_per_acq)]
    zprojs = [np.mean(acq, 0) for acq in acqs]
    
    return zprojs

def save_zprojs(zprojs, path):
    
    folder, orig_name = os.path.split(path)
    basename, _ = os.path.splitext(orig_name)
    
    output_folder = os.path.join(folder, "z_projections")
    os.mkdir(output_folder)
    
    for i, zproj in enumerate(zprojs):
        name = basename + "_" + str(i) + ".tif"
        zproj_path = os.path.join(output_folder, name)
        tifffile.imwrite(zproj_path, zproj)

def parse_tiff(arg):

    if os.path.exists(arg):
        
        if arg.endswith('.tiff') or arg.endswith('.tif'):
            return arg
        
        else:
            raise FileNotFoundError("The file is not a tiff")
            
    else:
        raise FileNotFoundError

def parse_frames_per_acq(arg):
    
    try:
        
        arg = int(arg)
        return arg
            
    except ValueError:
        
        raise NameError("frames per acquisition needs to be an integer")

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No tiff specified")
    
    if len(sys.argv) == 2:
        
        raise KeyError("Frames per acquisition not set")
        
    if len(sys.argv) == 3:
        
        path = parse_tiff(sys.argv[1])
        frames_per_acq = parse_frames_per_acq(sys.argv[2])
        
    return path, frames_per_acq

if __name__ == "__main__":
    
    run()

    
