##create experimental design for single.object.1000 experiment
import glob
from scipy.io import loadmat
import os
from numpy import random
from experimental_design.src.experiments import fmri_experiment, make_design_matrix

base_directory = '/Users/tnaselar/Data/Presentation/addiction.vision/'
blank_screen = 'rest_frame.bmp'
seconds_per_state = 2  ##a "state" is either show a cue, show a non-cue, or show a blank 
vols_per_state = 1
frames_per_state = 8 ##250 msec per frame (4 Hz framerate)
image_state_dynamics = [3, 2, 3] ##per active state
number_of_blank_frames = frames_per_state ##per blank state
number_of_stim_frames_pcp = frames_per_state ##to accomadate flashing stim will be broken up with one blank so we split into two
number_of_unique_stimuli = 8 # 4 cues , 4 non-cues
number_of_cue_stimuli = number_of_unique_stimuli/2 
number_of_non_cue_stimuli = number_of_unique_stimuli-number_of_cue_stimuli
number_of_reps_per_unique_stimulus = 8 #each image shown 8 times
blank_states = [5, 1, 5] #5 blanks at start, ~1 blank per isi, 5 blanks at end
image_dir = '/Users/tnaselar/Data/Presentation/addiction.vision/'
smoker_image_frames = glob.glob(image_dir+'msmq*.bmp') ##males only!
control_image_frames = glob.glob(image_dir+'mcon*.bmp') ##males only!
number_of_runs = 4

def blank_state():
	return [blank_screen]*number_of_blank_frames

def image_state(current_image):
	return [current_image]*image_state_dynamics[0]+[blank_screen]*image_state_dynamics[1]+[current_image]*image_state_dynamics[2]

##all smoker images
smoke_dx = list(random.permutation(len(smoker_image_frames)))
control_dx = list(random.permutation(len(control_image_frames)))

for rr in range(number_of_runs):
	run_name = 'run_%d' %(rr)
	##create design matrix: the balance of cues / non-cues is determined by the images in the image folder
	design_matrix = make_design_matrix(number_of_unique_stimuli, number_of_reps_per_unique_stimulus, blank_states = blank_states, seconds_per_state = seconds_per_state)
	##create frame list
	img_stim_list = []
	img_stim_list.append(blank_state()) ##<<WART: the "blank" state must always be first in the list! 
	cnt = number_of_cue_stimuli
	while cnt:
		random_index = smoke_dx.pop()
		current_image = os.path.split(smoker_image_frames[random_index])[1] ##this is equal to the image_id of the parent image for this object
		img_stim_list.append(image_state(current_image))
		cnt -= 1
	cnt = number_of_non_cue_stimuli
	while cnt:
		random_index = control_dx.pop()
		current_image = os.path.split(control_image_frames[random_index])[1] ##this is equal to the image_id of the parent image for this object
		img_stim_list.append(image_state(current_image))
		cnt -= 1


	##instaniate an fmri_experiment object
	run = fmri_experiment(design_matrix, img_stim_list, seconds_per_state, vols_per_state)

	##use object to build frame file and write it
	run.print_frame_list(base_directory+'%s_frame_list.txt' % (run_name))
	run.save_design_matrix(base_directory+'%s_design_matrix.npy' % (run_name))

