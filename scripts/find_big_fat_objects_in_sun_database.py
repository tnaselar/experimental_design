##===create object montages
from PIL import Image
from object_parsing.src import image_objects as imo
from object_parsing.src.image_objects import number_of_object_pixels
import glob
import os
im_dir = '/musc.repo/SUN/sun_images/'
mask_dir = '/musc.repo/SUN/mask_sun/'
file_list = '/musc.repo/Data/shared/query/'


background_image = '/Data/7T.cmrr/Presentation/pictures/-999999.png'
SIDE = 500
save_to = '/Data/tmp/sun_candidates/'

images = []
masks = []
idx = []
labels = []
for kk in glob.glob(file_list+'*.txt'):
  with open(kk,'r') as ff:
    flz = ff.readlines()
  flz = [ii.replace('\n','').strip().split('\t') for ii in flz]
  while flz:
    foo = flz.pop()
    images.append(im_dir+foo[0]+'/'+foo[1]) 
    masks.append(mask_dir+foo[1].replace('.jpg', '.png').replace('sun_', 'mask.sun_'))
    idx.append(int(foo[2]))
    labels.append(os.path.split(kk)[-1].replace('.txt', '').strip())


##montage geometry
SIDE = 1000
scaling_factor = 1
grid_spacing = 5
min_obj_size = 20
max_obj_size = 150

##object condition
min_size_in_original = 500**2/5 ##number of pixels
purity_fraction = 0.3 ##what fraction of pixels in the cropped box are covered by current object?
mask_margin = 11
presentation_radius = 300


    
 
##find keepers
bad = []
while masks:
  lbl = labels.pop()
  oo = imo.one_object(images.pop(), masks.pop(), idx.pop())
  cov = oo.pixel_coverage()
  pur = oo.object_purity()
  print '---------coverage: %0.6d, purity: %0.6f' %(cov, pur) 
  if (cov >= min_size_in_original) & (pur >= purity_fraction):
    print'--------------got one!'
    try:
      screen = imo.make_a_blank(SIDE, 0, 'RGB')
      oo.set_radius(presentation_radius).set_margin(mask_margin).paste_object_to_screen(screen, (SIDE/2, SIDE/2))
      screen.save(save_to+'%s.%s.%0.3d.png' %(lbl, os.path.split(oo.object_context.filename)[1].replace('.jpg', '').strip(), oo.source_id_number))
    except:
      print('----nope')
      1/0
      bad.append(save_to+'%s.%s.%0.3d.png' %(lbl, os.path.split(oo.object_context.filename)[1].replace('.jpg', '').strip(), oo.source_id_number))

###make pictures of keepers
#while keepers:
  #current_item = keepers.pop()
  #current_mask = current_item[0]
  #_,image_id = os.path.split(current_mask)
  #current_image = im_dir+image_id
  #current_id = current_item[1]
  #try:
    #current_label = open(label_dir+image_id.replace('png', 'labels.txt'), 'r').readlines()[current_id-1].replace('\n', '').strip()
    #current_category = open(label_dir+image_id.replace('png', 'categories.txt'), 'r').readlines()[current_id-1].replace('\n', '').strip()
    #obj = imo.one_object(current_image, current_mask, current_id, mask_margin = mask_margin, object_background = background_contrast)
    #obj.set_radius(presentation_radius)
    ##obj.object_image.save(save_to+'%s.%s.%0.3d.%s' %('x', 'y', current_id, image_id)) 
    #obj.object_image.save(save_to+'%s.%s.%0.3d.%s' %(current_category, current_label, current_id, image_id)) 
  #except:
    #print 'label or category file missing. skip'
    

  
