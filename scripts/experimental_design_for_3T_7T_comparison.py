##create experimental design for imagery rf experiment with the colored boxes, July 2014
import glob
from scipy.io import loadmat
import os
from numpy import random
from experimental_design.src.experiments import fmri_experiment, make_design_matrix


DO NOT RUN THIS AGAIN UNLESS YOU MEAN IT


base_directory = '/musc.repo/mri/3T.vs.7T.cmrr/'
selected_stimulus_matlab_file = base_directory+'stimDxTrnVal.mat'
stim_dict = loadmat(selected_stimulus_matlab_file)
training_img_list = list(stim_dict['stimDxTrn'][0])
validation_img_list = list(stim_dict['stimDxVal'][0])

blank_screen = '000000.png'
seconds_per_state = 1.5  ##a "state" is either show an image, or show a blank 
vols_per_state = 1
frames_per_state = 6 ##assume 4 Hz presentation.
number_of_unique_stimuli_training = 85 # 
number_of_unique_stimuli_validation = 10 # 
number_of_reps_per_unique_stimulus_training = 1 #each image shown 1 time per run
number_of_reps_per_unique_stimulus_validation = 4 #each image shown 4 times per run

number_of_training_sets = 14    ##a set is a group of runs with the same stimuli but in different order
number_of_validation_sets = 16
number_of_runs_per_set = 2

isi = [5, .15, 5] #5 blanks at start, ~1 blank per isi, 5 blanks at end

def stim_state(cue):
  return ['%0.6d.png' %(cue)]*frames_per_state 
  
def blank_state():
  from numpy import random
  return [blank_screen]*frames_per_state
  
##construct training runs
set_number = 1
while training_img_list:
  img_stim_list = []
  img_stim_list.append(blank_state())
  for ii in range(number_of_unique_stimuli_training):
    img_stim_list.append(stim_state(training_img_list.pop()))
  for ii in range(number_of_runs_per_set):
    print 'training_frame_file_set%0.2d_run%0.2d.txt' %(set_number, ii+1)
    design_matrix = make_design_matrix(number_of_unique_stimuli_training, number_of_reps_per_unique_stimulus_training, blank_states = isi, seconds_per_state = seconds_per_state)
    print '\n'
    run = fmri_experiment(design_matrix, img_stim_list, seconds_per_state, vols_per_state)
    run.print_frame_list(base_directory+'/training_frame_file_set%0.2d_run%0.2d.txt' %(set_number, ii+1))  
    run.save_design_matrix(base_directory+'/training_desing_matrix_set%0.2d_run%0.2d' %(set_number, ii+1))
  set_number += 1

##construct validation runs
set_number = 1
while validation_img_list:
  img_stim_list = []
  img_stim_list.append(blank_state())
  for ii in range(number_of_unique_stimuli_validation):
    img_stim_list.append(stim_state(validation_img_list.pop()))
  for ii in range(number_of_runs_per_set):
    print 'validation_frame_file_set%0.2d_run%0.2d.txt' %(set_number, ii+1)
    design_matrix = make_design_matrix(number_of_unique_stimuli_validation, number_of_reps_per_unique_stimulus_validation, blank_states = isi, seconds_per_state = seconds_per_state)
    print '\n'
    run = fmri_experiment(design_matrix, img_stim_list, seconds_per_state, vols_per_state)
    run.print_frame_list(base_directory+'/validation_frame_file_set%0.2d_run%0.2d.txt' %(set_number, ii+1))  
    run.save_design_matrix(base_directory+'/validation_desing_matrix_set%0.2d_run%0.2d' %(set_number, ii+1))
  set_number += 1  