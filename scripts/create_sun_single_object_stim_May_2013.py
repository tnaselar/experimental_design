##here we are converting the training and testing frame (or "conditions") files from the 7T Nov2011 experiment for use in
##in a single object experiment circa May 2013. this code was used to generate the psychopy "conditions.csv" file for the 500x500 experiment.
import os
import glob


location_of_original_frame_files = '/musc.repo/mri/3T.musc/Presentation/May.2013/frame_files/old/'
location_of_pics = '/musc.repo/mri/3T.musc/Presentation/May.2013/pics/'

save_new_frame_files_to = '/musc.repo/mri/3T.musc/Presentation/May.2013/frame_files/'
variable_name_in_first_row = ['image'] ##<<this is for psychopy

stimulus_computer_path = '/home/runner/sun_stim/pics/'



##=============training
all_trn_frame_files = glob.glob(location_of_original_frame_files+'*trn*')
list_of_pics = glob.glob(location_of_pics+'sun*')


dict_of_pic_replacements = {'000000.png' : '000000.png'}


#def get_new_image(old_image, image_list, a_dict):
  #if not a_dict.has_key(old_image):
    #foo,a_dict[old_image] = os.path.split(image_list.pop())
    #a_dict['-999999.png'] = 'background.'+a_dict[old_image]
  #return a_dict
    
#num = 0
#for frame_file in all_trn_frame_files:
  #with open(frame_file, 'r') as ff:
    #frames = ff.readlines()
  #frames = [ss.replace('\n', '') for ss in frames]
  #frames.reverse() ##<<makes it easier to deal with -99999 
  ##states = [frames[ii:ii+10] for ii in xrange(0,len(frames),10)]
  #new_frame_list = [get_new_image(ii, list_of_pics, dict_of_pic_replacements)[ii] for ii in frames]
  #new_frame_list.reverse()
  #new_file = open(save_new_frame_files_to+'trn%0.3d.txt' %(num), 'wb')
  #new_file.writelines(['%s\n' % item for item in new_frame_list])
  #new_file.close()
  #num += 1

##=============validation
  
##==========imagery
list_of_img_pics = \
['001133.png',
 '001175.png',
 '002954.png',
 '003084.png',
 '003260.png',
 '003275.png',
 '003330.png',
 '003415.png',
 '003560.png',
 '003562.png',
 '003974.png',
 '004194.png']

frame_file = glob.glob(location_of_original_frame_files+'img.txt')

def get_new_image(old_image, image_list, a_dict):
  if not a_dict.has_key(old_image):
    new_im = os.path.split(image_list.pop())[1:][0]
    a_dict[old_image] =  'label.background.'+new_im
    a_dict['200000.png'] = 'background.'+new_im
    a_dict[old_image.replace('-','').strip()] = new_im
  elif old_image == '-999999.png': 
    a_dict['200000.png'] = '000000.png'
  else:
    a_dict['200000.png'] = a_dict[old_image].replace('label.','').strip()
  return a_dict

with open(frame_file[0], 'r') as ff:
  frames = ff.readlines()
frames = [ss.replace('\n', '') for ss in frames]


##img001.txt
img1_replacements = {'000000.png' : '000000.png', '-999999.png' : '000000.png'}
new_frame_list = [get_new_image(ii, list_of_img_pics, img1_replacements)[ii] for ii in frames]
new_frame_list = [stimulus_computer_path+ii for ii in new_frame_list]
new_frame_list = variable_name_in_first_row + new_frame_list
new_file = open(save_new_frame_files_to+'img001.txt', 'wb')
new_file.writelines(['%s\n' % item for item in new_frame_list])
new_file.close()

##img002.txt
img2_replacements = {'000000.png' : '000000.png', '-999999.png' : '000000.png'}
new_frame_list = [get_new_image(ii, list_of_img_pics, img2_replacements)[ii] for ii in frames]
new_frame_list = [stimulus_computer_path+ii for ii in new_frame_list]
new_frame_list = variable_name_in_first_row + new_frame_list
new_file = open(save_new_frame_files_to+'img002.txt', 'wb')
new_file.writelines(['%s\n' % item for item in new_frame_list])
new_file.close()


with open(location_of_original_frame_files+'imgVal.txt', 'r') as ff:
  frames = ff.readlines()

##imgVal001.txt
frames = [ss.replace('\n', '') for ss in frames]
new_frame_list = [get_new_image(ii, list_of_img_pics, img1_replacements)[ii] for ii in frames]
new_frame_list = [stimulus_computer_path+ii for ii in new_frame_list]
new_frame_list = variable_name_in_first_row + new_frame_list
new_file = open(save_new_frame_files_to+'imgVal001.txt', 'wb')
new_file.writelines(['%s\n' % item for item in new_frame_list])
new_file.close()

##imgVal002.txt
frames = [ss.replace('\n', '') for ss in frames]
new_frame_list = [get_new_image(ii, list_of_img_pics, img2_replacements)[ii] for ii in frames]
new_frame_list = [stimulus_computer_path+ii for ii in new_frame_list]
new_frame_list = variable_name_in_first_row + new_frame_list
new_file = open(save_new_frame_files_to+'imgVal002.txt', 'wb')
new_file.writelines(['%s\n' % item for item in new_frame_list])
new_file.close()


