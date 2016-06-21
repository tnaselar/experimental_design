##===create object montages
from PIL import Image
from object_parsing.src import image_objects as imo
from object_parsing.src.image_objects import number_of_object_pixels
import glob
import os
im_dir = '/Data/LotusHill2/pictures/'
mask_dir = '/Data/tmp/labeled_image_maps/'
label_dir = mask_dir
number_of_images = 500;
background_image = '/Data/7T.cmrr/Presentation/pictures/-999999.png'
SIDE = 500
save_to = '/Data/tmp/test_montage/'



##montage geometry
SIDE = 500
scaling_factor = 1
grid_spacing = 5
min_obj_size = 20
max_obj_size = 150

##object condition
min_size_in_original = 500**2/5 ##number of pixels
purity_fraction = 0.3 ##what fraction of pixels in the cropped box are covered by current object?
mask_margin = 11
background_contrast = False
presentation_radius = 300

#def grab_image(im_dir, mask_dir, image_range,this_min):
  #from numpy.random import randint
  #from numpy import ones
  #obj_size = 0
  #print this_min
  #while obj_size < this_min:
    #rand_im_id = randint(image_range[0], image_range[1], 1)
    #im = im_dir+'%0.6d.png' %(rand_im_id)
    #mask = mask_dir+'%0.6d.png' %(rand_im_id) #mask_dir+'tmp_mask.jpg'#
    #tmp_mask = Image.open(mask)
    #mx = max(find_object_values(tmp_mask))   ##get what will probably be the top mask
    #obj_size = imo.one_object(im,mask,mx).radius()
    #print obj_size
  #print '-------got one'
  #return im, mask, mx

def grab_image(mask_file):
  tmp_mask = Image.open(mask_file)
  for ii in find_object_values(tmp_mask):
    obj = imo.one_object(mask_file,mask_file,ii)
    cov = obj.pixel_coverage()
    pur = obj.object_purity()
    print '---------coverage: %0.6d, purity: %0.6f' %(cov, pur) 
    if (cov >= min_size_in_original) & (pur >= purity_fraction):
      print'--------------got one!'
      keepers.append([mask_file, ii])
    
    
def find_object_values(mask):
	'''
	object_values = find_object_values(mask)
	Find pixel values of each of the objects in an object mask
	Returns a numpy array containing the values. 
	len(object_values) = total number of objects in the mask
	'''
	from numpy import unique, array
	return unique(array(mask))

##find keepers
keepers = []
im_list = glob.glob(mask_dir+'*.png')
while im_list:
  grab_image(im_list.pop())

##make pictures of keepers
while keepers:
  current_item = keepers.pop()
  current_mask = current_item[0]
  _,image_id = os.path.split(current_mask)
  current_image = im_dir+image_id
  current_id = current_item[1]
  try:
    current_label = open(label_dir+image_id.replace('png', 'labels.txt'), 'r').readlines()[current_id-1].replace('\n', '').strip()
    current_category = open(label_dir+image_id.replace('png', 'categories.txt'), 'r').readlines()[current_id-1].replace('\n', '').strip()
    obj = imo.one_object(current_image, current_mask, current_id, mask_margin = mask_margin, object_background = background_contrast)
    obj.set_radius(presentation_radius)
    #obj.object_image.save(save_to+'%s.%s.%0.3d.%s' %('x', 'y', current_id, image_id)) 
    obj.object_image.save(save_to+'%s.%s.%0.3d.%s' %(current_category, current_label, current_id, image_id)) 
  except:
    print 'label or category file missing. skip'
    

  
