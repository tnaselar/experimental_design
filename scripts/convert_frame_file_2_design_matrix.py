# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#%load_ext autoreload
#%autoreload 2
import numpy as np
from experimental_design.src.experiments import fmri_experiment as fme
from scipy.io import savemat, loadmat
#%pylab inline

# <codecell>


# <codecell>

##experimental parameters
TR = 2
show_hz = 10

# <codecell>

base_location= '/Users/tnaselar/Data/Presentation/imagery.rf.7T.July.2014/'
save_location = '/musc.repo/scratch/'

# <codecell>

run_paths = ['imagery_001/frame_files/']
frames_per_TR = TR*show_hz
blank_frame = 'rest_frame_0.png'

for rr in run_paths:
    pcp_frame_file = base_location+rr+'pcp_frame_list.txt'
    img_frame_file = base_location+rr+'img_frame_list.txt'

    with open(pcp_frame_file) as f:
        pcp_frames = f.readlines()
    pcp_frames = map(lambda s: s.strip(), pcp_frames) ##strips the \n off the end of each string
    total_pcp_frames = len(pcp_frames)
    
    with open(img_frame_file) as f:
        img_frames = f.readlines()
    img_frames = map(lambda s: s.strip(), pcp_frames)
    total_img_frames = len(img_frames)
    
    ##determine the frame associated with each volume
    total_number_of_volumes = len(range(0, total_pcp_frames, frames_per_TR)) 
    print total_number_of_volumes ##<this is what I remember it should be

    ##unique list of frames, ordered by first appearance
    unique_frames = []
    for ff in pcp_frames:
        if ff not in unique_frames:
            unique_frames.append(ff)
    #unique_frames = list(np.unique(pcp_frames))
    unique_frames.pop(unique_frames.index(blank_frame)) ##pop the blank frame 
    number_of_unique_frames = len(unique_frames)

    ##build the design matrix
    design_matrix = np.zeros((number_of_unique_frames, total_number_of_volumes)) 
    cnt = 0
    for ii in range(0, total_pcp_frames, frames_per_TR):
        if pcp_frames[ii] == blank_frame:
            cnt += 1
            continue
        else:
            jj = unique_frames.index(pcp_frames[ii])
            design_matrix[jj,cnt] = 1
            cnt += 1
    #savemat(save_location+'design_matrix.mat', mdict = {'design_matrix': design_matrix})

# <codecell>
stim_list = [[ii]*20 for ii in [blank_frame]+unique_frames]
test_exp = fme(design_matrix, stim_list , 2, 1)

