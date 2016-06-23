
def make_design_matrix(number_of_states, number_of_reps, blank_states= [5, .5, 10], seconds_per_state=None):
  import numpy as np
  '''a simple experimental design matrix with random inter-stimulus intervals.
  make_design_matrix(number_of_states, number_of_reps, blank_states= [10, 0.5, 10], seconds_per_state=none)
  blank_states = [number_at_beginning, probability_during, number at end] the number of TRs
  for each isi is determined by the middle argument as 1+poissrand(blank_states[1]) 
  note that seconds_per_state is for convenience if you want a print-out of how long the experiment will take
  does not allow back-to-back repeats of conditions.
  '''
  time_line = [0]*blank_states[0]
  ##create time-line by popping off random states. don't allow back-to-back repeats.
  for ii in range(number_of_reps):
  	rep = list(np.random.permutation(np.arange(number_of_states)+1))
  	while len(rep):
  	  time_line.append(rep.pop())
  	  chance = np.random.random();
  	  num_blanks = 1+np.random.poisson(blank_states[1])
  	  time_line.extend([0]*num_blanks)
  time_line.extend([0]*blank_states[-1])
  time_length = len(time_line)
  if seconds_per_state:
    print 'length of experiment: %d states and %f seconds = %f mintues' % (time_length, time_length*seconds_per_state, time_length*seconds_per_state/60.)
  else:
    print 'length of experiment: %d states' % (time_length)
  ##create the design matrix
  design_matrix = np.zeros((number_of_states, time_length))
  cnt = 0
  while time_line:
    dx = time_line.pop(0)
    if dx:
      design_matrix[dx-1,cnt] = 1
    cnt += 1
  return design_matrix


class fmri_experiment:
  def __init__(self, design_matrix, stim_list, seconds_per_state, vols_per_state):
    self.stim_list = stim_list ##<<WART: the "blank" state must always be first in the list!
    self.seconds_per_state = seconds_per_state
    self.vols_per_state = vols_per_state
    self.design_matrix = design_matrix
    self.frame_list = self.build_frame_list()


    
  def build_frame_list(self):
    from numpy import where
    frame_list = []
    for ii in self.design_matrix.T: ##<<iterate over columns
      dx = where(ii)[0]+1	##+1 because we use the first slot for the blank state
      if not dx:
      	dx = 0
      frame_list.extend(self.stim_list[dx])
    return frame_list
    
  def print_frame_list(self, frame_list_file):
    with open(frame_list_file, 'w') as ff: 
      for item in self.frame_list:
	ff.write("%s\n" % item)
	
  def save_design_matrix(self, des_mat_file):
    from numpy import save
    save(des_mat_file, self.design_matrix)

