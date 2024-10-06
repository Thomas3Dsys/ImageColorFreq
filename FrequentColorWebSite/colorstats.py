from PIL import Image
import numpy as np
from collections import OrderedDict
from itertools import islice

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(rgb[0],rgb[1],rgb[2])


def get_image_top_colors(dir:str, img_src:str, amt:int):
    """Returns a dictionary with two main sub-dictionary entries:
        stats - dictionary of stats about the image... like total unique colors.
        colors-  dictionary of the top (quantity equal to the amt parameter) colors ordered by ocurrence
    """
    
    #print(f"path:{dir}/{img_src}")
    im = Image.open(f"{dir}/{img_src}").convert('RGB')
    im_matrix= np.asarray(im)
    resolution = f"{im.size[0]} x {im.size[1]}"
    total_pixels = im.size[0] * im.size[1]

    # Reshape from matrix to linear
    rgb_pixels = im_matrix.reshape(-1, 3)
    
    # Get unique colors and their counts
    unique_colors, counts = np.unique(rgb_pixels, axis=0, return_counts=True)
    color_count= len(unique_colors)
    
    #Merge counter colors back to an ndarray
    unique_color_counts = np.column_stack((unique_colors,counts))
    sorted_counts  = unique_color_counts[unique_color_counts[:,3].argsort()[::-1]]
    #index, count

    #get most frequent colors
    top_sorted_counts = sorted_counts[:amt]
    
    #get hex values
    rbg_top = {rgb_to_hex(cell[0:3]):int(cell[3]) for cell in top_sorted_counts}

    stats = {}
    stats["stats"] = {
                      "unique colors": color_count,
                      "pixels": total_pixels,
                      "resolution": resolution
                      }
    #key is hex, value is count
    stats["colors"] = rbg_top 
    
    return stats

    




