import os
import glob
import numpy as np
import math
from PIL import Image, ImageChops, ImageDraw
import object_parsing.src.image_objects as imo

##little boxes. there's a pink one and a blue one and a green one and a yellow one...
pink = [(226,204,225),(256,128),(131,241), (368.97, 241)]
black = [(0,0,0), (382,130)]
green = [(186, 216,115), (384, 256), (259,131), (259,369)]
white = [(255,255,255), (382,382)]
orange = [(244,185,126), (256,384), (131, 259), (368.97, 259)]
sky = [(152, 217, 238), (130, 382)]
purple = [(147, 134, 178), (128, 256), (241, 131), (241, 369)]
yellow = [(244, 235, 47), (130.119,130.118)]
boxes = dict(pink=pink, black=black, green=green, white=white, orange=orange, sky=sky, purple=purple, yellow=yellow)


def draw_box_corners(im,size=12):
	import ImageDraw
	draw = ImageDraw.Draw(im)
	embiggen = lambda x: tuple(np.array(x)+size)
	for colors in ['pink', 'green', 'orange', 'purple']:
		c1 = boxes[colors][2]
		c2 = boxes[colors][3]
		fill = boxes[colors][0]
		draw.rectangle([c1,embiggen(c1)], fill=fill)
		draw.rectangle([c2,embiggen(c2)], fill=fill)
		
imagery_run_folders = glob.glob('/Users/tnaselar/Data/Presentation/single.object.boxes/pics/single.object.1000.med.font/imagery_*')
original_image_folder = '/Users/tnaselar/Data/Pictures/LotusHill2/pictures/'
original_object_map_folder = '/Users/tnaselar/Data/Pictures/LotusHill2/labeled_image_maps/'

image_file_names = '%s.%0.3d.%0.2d.%s.png' ##syntax is (image_id, pixel_id, instance_id = 1 - number_of_locations, type=image/cat_cue/loc_cue,  

save_to_dir = '/Users/tnaselar/Data/Presentation/single.object.boxes/pics/single.object.1000.med.font/'

##run types
##img_1 - img_8
##pcp_1 - pcp_8

##trn_1 - trn_8

##size of visual field in pixels
SIDE = 400
CENTER = (200,200)

##parameters determining visual field of view
# distance_to_screen = 10. #(cm)
# size_on_screen = SIDE/1920.*11.43#11.43 cm is the size of the full 1920x1080 screen projection. #(cm)
# visual_subtend = math.degrees(math.atan((size_on_screen/2)/distance_to_screen))*2. ##degrees
# pixels_per_degree = SIDE/visual_subtend ##<<comes out to about 32 pixels per degree

##object presentation parameters
mask_margin = 11
box_centers = [boxes[colors][1] for colors in boxes.keys()]
radius = 238./2. #math.sqrt(238**2+238**2)/2.
box_colors = [boxes[colors][0] for colors in boxes.keys()]

##cue and background parameters
fixation_dot_size = 3		##about .25 deg
fixation_dot_color = tuple([255]*3)
background_image_color = 128 #tuple([128]*3)
category_cue_font_size = .12#.05 ##minimum readable
background_image = Image.open('/Users/tnaselar/Data/Presentation/single.object.boxes/Boxes.400.png')
rest_label = 'XXXXXX'

# imo.reveal_center(background_image, fixation_dot_size, fixation_dot_color)

##for the img and pcp runs
imagery_run_folders = ['/Users/tnaselar/Data/Presentation/single.object.boxes/pics/single.object.1000.med.font/imagery_001']
while imagery_run_folders:
  cur_dir = imagery_run_folders.pop()
  list_of_images = glob.glob(cur_dir+'/*.txt')
#   list_of_images = [list_of_images[0]]
  save_to = save_to_dir+cur_dir[-11:]
  while list_of_images:
    current_image = list_of_images.pop()
    image_id = os.path.split(current_image)[1].split('.')[0]
    with open(current_image, 'r') as ff:
      lbl = ff.readline().replace('\n', '').strip()
    background_image.save(save_to+'/frame_files/'+'blank.png')
    object_specs = os.path.split(glob.glob(cur_dir+'/*'+image_id+'*.png')[0])[1].split('.')
    object_id = int(object_specs[-3])
    ##create a "one_object" instance
    oo = imo.one_object(original_image_folder+image_id+'.png', original_object_map_folder+image_id+'.png', object_id)
    ##create a composition for the object
    tc = imo.boring_composition(SIDE=SIDE, locations=box_centers, radius = radius)
    ##create a montage for presenting the object
    mo = imo.montage(SIDE, background_image, tc)
    ##create the list
    mo.object_list = [oo]*tc.number_of_objects 
    ##make the pictures with objects, location cues and no labels for pcp runs
    try:
    	object_pictures = mo.show_picture(mask_margin=mask_margin)
    except:
		1/0
    ##show them for good measure
    mo.show_picture(flat=True)[0].show()
    cnt = 0
    ##add text to each pasted object frame and save
    for ii,op in enumerate(object_pictures):
      imo.put_text(op, message = lbl, position = (.5, .5), fill=box_colors[ii],size = category_cue_font_size).save(save_to+'/frame_files/'+image_file_names % (image_id,  object_id, cnt,'image'))
      copy_background = Image.open('/Users/tnaselar/Data/Presentation/single.object.boxes/Boxes2.png')
      imo.put_text(copy_background, message = lbl, position = (.5, .5), fill=box_colors[ii],size = category_cue_font_size).save(save_to+'/frame_files/'+image_file_names % (image_id,  object_id, cnt,'cue'))
      cnt += 1
  ##make a "rest" frame
  copy_background = Image.open('/Users/tnaselar/Data/Presentation/single.object.boxes/Boxes2.png')
  imo.put_text(copy_background, message=rest_label, position=(0.5,0.5)).save(save_to+'/frame_files/'+'rest_frame.png')
      
    ##make pictures with location cues only for both the pcp and img runs
#     cue_pictures = mo.show_picture(mask_margin=mask_margin, reveal_corners = location_cue_size, locations_only = True)
#     cnt = 0
#     for cp in cue_pictures:
#       ##location cues only for img.
#       imo.reveal_center(cp, fixation_dot_size, fill=fixation_dot_color).save(save_to+'/frame_files/'+image_file_names % (image_id, object_id, cnt, 'location'))
#       ##location cues + labels for img and pcp
#       imo.put_text(cp, message = lbl, position = (.5, .5), size = category_cue_font_size).save(save_to+'/frame_files/'+image_file_names % (image_id, object_id, cnt,'cue'))
#       cnt += 1

  #mo.dump(save_to+montage_object_file...)

##for the trn runs

##create a "simple_composition" and a montage
#sc = imo.simple_composition(len(list_of_trn_objects), max_radius = max_object_radius, min_radius=min_object_radius)
#mo = imo.montage(SIDE, imo.make_a_blank(SIDE,background_image_color,'RGB'), sc) ##<< this will probably kill memory
#while list_of_trn_objects:
  #object_specs = list_of_trn_objects.pop()
  #image_id = object_specs[0]
  #object_id = object_specs[1]
  #number_of_locations = object_specs[2]
  ###collect new object
  #mo.object_list.append(imo.one_object(image_folder+image_id, mask_folder+image_id, object_id))
  ###create a montage for presenting the object
  
###make the pictures with objects and location cues and no labels for pcp runs
#object_pictures = mo.show_picture(mask_margin=mask_margin, reveal_corners = location_cue_size)
#for op in object_pictures:
  #reveal_center(op, fixation_dot_size, fill=fixation_dot_color).save(save_to+image_file_names ...)
  
###make pictures with location cues only for both the pcp and img runs
#cue_pictures = mo.show_picture(mask_margin=mask_margin, reveal_corners = location_cue_size, location_only = True)
#for cp in cue_pictures:
  ###location cues + dummy label
  #cp = reveal_center(cp, fixation_dot_size, fill=fixation_dot_color)
  #imo.put_text(cp, message = dummy_label, position = CENTER, size = category_cue_font_size).save(save_to+image_file_names...)

#mo.dump(save_to+montage_object_file...)
    
 	