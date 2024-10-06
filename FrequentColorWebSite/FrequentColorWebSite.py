from colorstats import get_image_top_colors
import os
 
img_stats = get_image_top_colors(f'{os.getcwd()}/static/assets/uploads/',"th_breakout.png", 20)
    
color_count = img_stats["stats"]["total"] 
    
top_color_stats = [(k, v) for k, v in img_stats["colors"].items()]

pass
