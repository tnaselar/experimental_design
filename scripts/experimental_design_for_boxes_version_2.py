##create experimental design for imagery rf experiment with the colored boxes, July 2014
import glob
from scipy.io import loadmat
import os
from numpy import random
from experimental_design.src.experiments import fmri_experiment, make_design_matrix
base_directory = '/Users/tnaselar/Data/Presentation/imagery.rf.7T.July.2014/'
imagery_run_directories = glob.glob(base_directory+'imagery_*')
blank_screen = 'rest_frame_%d.png'
number_of_blank_screens = 4 #there are several jittered versions of the background to combat retinal fatigue
seconds_per_state = 2  ##a "state" is either show a cue, show an image, or show a blank 
vols_per_state = 1
frames_per_state = 20 ##100 msec per frame
number_of_cue_frames = frames_per_state ##per active state
number_of_blank_frames = frames_per_state ##per blank state
number_of_stim_frames_pcp = frames_per_state ##to accomadate flashing stim will be broken up with one blank so we split into two
number_of_unique_stimuli = 64 # 8 images @ 8 locations
number_of_reps_per_unique_stimulus = 2 #each image shown 1 time at each location
blank_states = [5, .4, 5] #5 blanks at start, ~1 blank per isi, 5 blanks at end

def imagery_state(cue):
  return [cue]*number_of_cue_frames #+[location]*number_of_stim_frames_img
  
def pcp_state(image):
  return [image]*number_of_stim_frames_pcp

  ##for each run we have
  ##folder ~ cannonical
		##cannoncial images of selected objects
		##text files giving label name for cannonical object
  ##folder ~ frame_images
	     ##the various frames containning scaled/offset pictures of cannonical objects, their cues, and a blank.
  ##designmatrix: a .mat file with a design matrix in it.

def blank_state():
  from numpy import random
  return [blank_screen % (0)]*number_of_blank_frames
  #return [blank_screen % (random.randint(0,high=number_of_blank_screens)) for ii in range(number_of_blank_frames)]

##create design matrix
#design_matrix = make_design_matrix(number_of_unique_stimuli, number_of_reps_per_unique_stimulus, blank_states = [5, .3, 5], seconds_per_state = 2)

##for each run folder
while imagery_run_directories:
  design_matrix = make_design_matrix(number_of_unique_stimuli, number_of_reps_per_unique_stimulus, blank_states = [5, .3, 5], seconds_per_state = 2)
  current_dir = imagery_run_directories.pop()
  img_stim_list = []
  img_stim_list.append(blank_state())
  pcp_stim_list = []
  pcp_stim_list.append(blank_state())
  image_frames = glob.glob(current_dir+"/frame_files/*image*")
  image_frames.sort()
  cue_frames = glob.glob(current_dir+"/frame_files/*cue*")
  cue_frames.sort()
  dx = list(random.permutation(len(image_frames)))
  while dx:
    random_index = dx.pop()
    current_image = os.path.split(image_frames[random_index])[1] ##this is equal to the image_id of the parent image for this object
    current_cue = os.path.split(cue_frames[random_index])[1]
    img_stim_list.append(imagery_state(current_cue))
    pcp_stim_list.append(pcp_state(current_image))
  ##instaniate an fmri_experiment object
  img_run = fmri_experiment(design_matrix, img_stim_list, seconds_per_state, vols_per_state)
  pcp_run = fmri_experiment(design_matrix, pcp_stim_list, seconds_per_state, vols_per_state)
  ##use object to build frame file and write it
  img_run.print_frame_list(current_dir+'/frame_files/img_frame_list.txt')
  pcp_run.print_frame_list(current_dir+'/frame_files/pcp_frame_list.txt')
  
  img_run.save_design_matrix(current_dir+'/frame_files/design_matrix')