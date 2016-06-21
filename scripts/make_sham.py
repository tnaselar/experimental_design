##create stimuli for single.object.1000 experiment
import os
import glob
import numpy as np
import math
from PIL import Image, ImageChops, ImageDraw
import object_parsing.src.image_objects as imo
from object_parsing.src.image_objects import put_text

sham_run = '/musc.repo/mri/3T.musc/Presentation/single.object.1000.med.font/imagery_008/frame_files'
cue_pictures = glob.glob(sham_run+'/*cue*')
save_to = '/Data/tmp/sham/'

#for ii in cue_pictures:
  #im = Image.open(ii)
  #put_text(im, message='sailbt', position=(.5,.5),size=.08)
  #put_text(im, message='rockss', position=(.5,.5),size=.08)
  #put_text(im, message='emupck', position=(.5,.5),size=.08)
  #put_text(im, message='picgrp', position=(.5,.5),size=.08)
  #put_text(im, message='redman', position=(.5,.5),size=.08)
  #put_text(im, message='bigcld', position=(.5,.5),size=.08)
  #put_text(im, message='hippot', position=(.5,.5),size=.08)
  #put_text(im, message='thedam', position=(.5,.5),size=.08)
  #im.save(save_to+os.path.split(ii)[1])
  
  

foo = open(sham_run+'/img_frame_list.txt', 'r')
image_frames = foo.readlines()

sham_frame_file = open(save_to+'/sham_frame_list.txt','w')
sham_frames = []
while image_frames:
  cur = image_frames.pop(0)
  if not 'cue' in cur:
    sham_frames.append(cur)
  else:
    sham_frames.append(cur.replace('cue','sham'))
foo.close()

#imagery_run_folders = glob.glob('/Data/tmp/single.object.1000.x.large.font/imagery_*')#'/musc.repo/mri/3T.musc/Presentation/single.object.1000/imagery_*')
#original_image_folder = '/Data/LotusHill2/pictures/'
#original_object_map_folder = '/Data/LotusHill2/labeled_image_maps/'

#image_file_names = '%s.%0.3d.%0.2d.%s.png' ##syntax is (image_id, pixel_id, instance_id = 1 - number_of_locations, type=image/cat_cue/loc_cue,  

#save_to_dir = '/Data/tmp/single.object.1000.x.large.font/'## will ultimately be move here: '/musc.repo/mri/3T.musc/single.object.1000/'

###run types
###img_1 - img_8
###pcp_1 - pcp_8

###trn_1 - trn_8

###size of visual field in pixels
#SIDE = 1000
#CENTER = (500,500)

###parameters determining visual field of view
#distance_to_screen = 10. #(cm)
#size_on_screen = SIDE/1920.*11.43#11.43 cm is the size of the full 1920x1080 screen projection. #(cm)
#visual_subtend = math.degrees(math.atan((size_on_screen/2)/distance_to_screen))*2. ##degrees
#pixels_per_degree = SIDE/visual_subtend ##<<comes out to about 32 pixels per degree

###object presentation parameters
#mask_margin = 11
#min_object_radius = 32 ##<<smallest object will be ~1 deg across
#max_object_radius = 320 ##<<largest object will be ~10 deg. across
#try_this_many = 250 ##<<how long are you willing to spend randomizing size/location
#number_of_locations = 9

###cue and background parameters
#fixation_dot_size = 3		##about .25 deg
#fixation_dot_color = tuple([255]*3)
#background_image_color = 128 #tuple([128]*3)
#location_cue_size = 10
#category_cue_font_size = .12#.05 ##minimum readable
#background_image = imo.make_a_blank(SIDE, background_image_color, 'RGB') ##a gray or black screen with a fixation dot.
#imo.reveal_center(background_image, fixation_dot_size, fixation_dot_color)


###make a map of the ideal coverage of visual field for each object
#target = Image.fromarray(np.zeros((SIDE,SIDE)).astype('uint8'))
#draw = ImageDraw.Draw(target)
#draw.ellipse([0,0,SIDE,SIDE],fill=255)
#target = np.array(target)/255


###for the img and pcp runs
#while imagery_run_folders:
  #cur_dir = imagery_run_folders.pop()
  #list_of_images = glob.glob(cur_dir+'/*.txt')
  #save_to = save_to_dir+cur_dir[-11:]
  #while list_of_images:
    #current_image = list_of_images.pop()
    #image_id = os.path.split(current_image)[1].split('.')[0]
    #with open(current_image, 'r') as ff:
      #lbl = ff.readline().replace('\n', '').strip()
    #background_image.save(save_to+'/frame_files/'+'blank.png')
    #object_specs = os.path.split(glob.glob(cur_dir+'/*'+image_id+'*.png')[0])[1].split('.')
    #object_id = int(object_specs[-3])
    ###create a "one_object" instance
    #oo = imo.one_object(original_image_folder+image_id+'.png', original_object_map_folder+image_id+'.png', object_id)
    ###create a "target_composition" for the object
    #tc = imo.target_composition(target.shape[0], number_of_locations, oo, target, max_radius = max_object_radius, min_radius = min_object_radius, try_this_many=try_this_many)
    ###create a montage for presenting the object
    #mo = imo.montage(SIDE, imo.make_a_blank(SIDE,background_image_color,'RGB'), tc)
    ###create the list
    #mo.object_list = [oo]*tc.number_of_objects 
    ###make the pictures with objects, location cues and no labels for pcp runs
    #object_pictures = mo.show_picture(mask_margin=mask_margin, reveal_corners = location_cue_size)
    ###show them for good measure
    #mo.show_picture(flat=True)[0].show()
    #cnt = 0
    #for op in object_pictures:
      #imo.reveal_center(op, fixation_dot_size, fill=fixation_dot_color).save(save_to+'/frame_files/'+image_file_names % (image_id,  object_id, cnt,'image'))
      #cnt += 1
      
    ###make pictures with location cues only for both the pcp and img runs
    #cue_pictures = mo.show_picture(mask_margin=mask_margin, reveal_corners = location_cue_size, locations_only = True)
    #cnt = 0
    #for cp in cue_pictures:
      ###location cues only for img.
      #imo.reveal_center(cp, fixation_dot_size, fill=fixation_dot_color).save(save_to+'/frame_files/'+image_file_names % (image_id, object_id, cnt, 'location'))
      ###location cues + labels for img and pcp
      #imo.put_text(cp, message = lbl, position = (.5, .5), size = category_cue_font_size).save(save_to+'/frame_files/'+image_file_names % (image_id, object_id, cnt,'cue'))
      #cnt += 1

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
    
 
