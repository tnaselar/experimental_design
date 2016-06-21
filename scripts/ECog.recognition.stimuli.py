import os
import glob
import numpy as np
import math
from PIL import Image, ImageChops, ImageDraw
import object_parsing.src.image_objects as imo
import random
import csv

##little boxes. there's a pink one and a blue one and a green one and a yellow one...
pink = [(228,161,194),(256,128),(131,241), (368.97, 241)]
black = [(0,0,0), (382,130)]
green = [(100, 189,99), (384, 256), (259,131), (259,369)]
white = [(255,255,255), (382,382)]
orange = [(246,136,31), (256,384), (131, 259), (368.97, 259)]
sky = [(0, 187, 220), (130, 382)]
purple = [(75, 46, 144), (128, 256), (241, 131), (241, 369)]
yellow = [(244, 235, 47), (130.119,130.118)]
boxes = dict(pink=pink, black=black, green=green, white=white, orange=orange, sky=sky, purple=purple, yellow=yellow)

viewing_distance = 72 #cm

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

image_file_names = '%s.%0.3d.%s.png' ##syntax is (image_id, pixel_id, type=image/cat_cue/loc_cue)  

save_to_dir = '/Users/tnaselar/Data/tmp/'

##run types
##img_1 - img_8
##pcp_1 - pcp_8

##trn_1 - trn_8

##size of visual field in pixels
SIDE = 1000
CENTER = (500,500)

##parameters determining visual field of view
distance_to_screen = 10. #(cm)
size_on_screen = SIDE/1920.*11.43#11.43 cm is the size of the full 1920x1080 screen projection. #(cm)
visual_subtend = math.degrees(math.atan((size_on_screen/2)/distance_to_screen))*2. ##degrees
pixels_per_degree = SIDE/visual_subtend ##<<comes out to about 32 pixels per degree

##object presentation parameters
mask_margin = 11
box_centers = [boxes[colors][1] for colors in boxes.keys()]
radius = SIDE/2. #math.sqrt(238**2+238**2)/2.
box_colors = [boxes[colors][0] for colors in boxes.keys()]
RIGHT_REPS_PER_IMAGE = 4
WRONG_REPS_PER_IMAGE = 4

##cue and background parameters
fixation_dot_size = 3		##about .25 deg
fixation_dot_color = tuple([255]*3)
background_image_color = 128 #tuple([128]*3)
category_cue_font_size = .12#.05 ##minimum readable


##labels for each image...I think
labels = {'003155':'flock of birds', \
		  '003252': 'red ants', \
		  '000723': 'students in a classroom', \
		  '003650': 'coral', \
		  '002227': 'old building', \
		  '003107': 'fire truck', \
		  '000190': 'water fountain', \
		  '003776': 'baby', \
		  '003889': 'crocodile', \
		  '003048': 'crouching boy', \
		  '000079': 'two beds', \
		  '001426': 'snowy trees and bushes', \
		  '003974': 'curious people', \
		  '004237': 'cheese toast', \
		  '000632': 'gloomy sky', \
		  '003138': 'walrus', \
		  '003195': 'towels', \
		  '003270': 'turtle', \
		  '003135': 'sleeping boy',\
		  '003118': 'monkey', \
		  '001100': 'grassy hill',\
		  '000709': 'boy scouts',\
		  '003874': 'flowers', \
		  '003361': 'motorcyle', \
		  '003990': 'smiling woman', \
		  '003238': 'vulture', \
		  '000907': 'red sofa', \
		  '002560': 'sports stadium', \
		  '001661': 'several puffy clouds', \
		  '002130': 'sunrise', \
		  '004150': 'neon sign', \
		  '003471': 'dolphin', \
		  '003569': 'hats',\
		  '003292': 'girl eating apple',\
		  '003235': 'fish market',\
		  '000718': 'audience', \
		  '001496': 'autumn trees', \
		  '002435': 'chips', \
		  '003206': 'killer whale',\
		  '002143': 'green sea', \
		  '004087': 'a hand', \
		  '003200': 'running horses', \
		  '003562': 'zebras', \
		  '002699': 'people on the street',\
		  '000642': 'highway', \
		  '001237': 'palm trees', \
		  '004189': '18', \
		  '001218': 'running creek',\
		  '003832': 'lizard face',\
		  '003922': 'man with hat', \
		  '003705': 'baby donkey', \
		  '001194': 'mountain range', \
		  '004138': 'men with hats and drums',\
		  '000175': 'hotel at night', \
		  '000378': 'fancy ceiling',\
		  '002185': 'ocean wave',\
		  '003140': 'ostriches',\
		  '003911': 'man with white beard',\
		  '003690': 'hippo', \
		  '001362': 'colorful boulders', \
		  '003283': 'crowd taking photos', \
		  '003039': 'big white dam', \
		  '003724': 'one big cloud',\
		  '000459': 'boats'}
		  
		  

# imo.reveal_center(background_image, fixation_dot_size, fixation_dot_color)

##for the img and pcp runs
while imagery_run_folders:
  cur_dir = imagery_run_folders.pop()
  list_of_images = glob.glob(cur_dir+'/*.txt')
#   list_of_images = [list_of_images[0]]
  save_to = save_to_dir+cur_dir[-11:]+'_'
  ##open a text file for writing
  ff= open(save_to+'.csv', 'wb')
  cf = csv.writer(ff)
  #put_this='image\ttext\tcorrAns\n'
  put_this = [['image', 'text', 'corrAns']]
  cf.writerows(put_this)
  while list_of_images:
    current_image = list_of_images.pop()
    image_id = os.path.split(current_image)[1].split('.')[0]
    object_specs = os.path.split(glob.glob(cur_dir+'/*'+image_id+'*.png')[0])[1].split('.')
    object_id = int(object_specs[-3])
    ##create a "one_object" instance
    oo = imo.one_object(original_image_folder+image_id+'.png', original_object_map_folder+image_id+'.png', object_id)
    background_image = imo.make_a_blank(SIDE, background_image_color, 'RGB')
    oo.set_margin(mask_margin).set_radius(radius).paste_object_to_screen(background_image, CENTER)
    save_image = image_file_names % (image_id,  object_id,'image')
    #background_image.save(save_to+save_image)
    ##now print this to the file 8 times. the first 4 times, use the correct label, the rest of the time use a random label
    right_reps = RIGHT_REPS_PER_IMAGE
    while right_reps:
    	#put_this = save_image+'\t%s\t%s\n' % (labels[image_id], 'n')
    	put_this = [[cur_dir[-11:]+save_image, labels[image_id], 'n']]
    	cf.writerows(put_this)
    	right_reps -= 1
    wrong_reps = WRONG_REPS_PER_IMAGE
    while wrong_reps:
    	#put_this = save_image+'\t%s\t%s\n' % (labels[random.choice(labels.keys())], 'm')
    	put_this = [[cur_dir[-11:]+save_image, labels[random.choice(labels.keys())], 'm']]
    	cf.writerows(put_this)
    	wrong_reps -= 1
  ff.close()
