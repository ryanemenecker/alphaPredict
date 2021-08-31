"""
Backend of the IDR machine learning predictor. Based partly
on code from Dan Griffith's IDP-Parrot from the Holehouse lab
(specifically the test_unlabeled_data function in train_network.py).
"""

# import packages for predictor
import sys
import os

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


# import modules that predictor depends on
from alphaPredict.backend import encode_sequence
from alphaPredict.backend import brnn_architecture


# set path for location of predictor. Using this in case I want to update the predictor or
# eventually make multiple predictors.
PATH = os.path.dirname(os.path.realpath(__file__))

# Setting predictor equal to location of weighted values.
predictor = "{}/networks/alpha_fold_networkV7_hs100_nL2_200e_all_prot.pt".format(PATH)

##################################################################################################
# hyperparameters used by when metapredict was trained. Manually setting them here for clarity.
##################################################################################################
# This is defined externally so its read in and loaded one time on the initial import
#
'''
network parameters for /networks/alpha_fold_networkV1.pt - 

device = 'cpu'
hidden_size = 10
num_layers = 1
dtype = 'residues'
num_classes = 1
encoding_scheme = 'onehot'
input_size = 20
problem_type = 'regression'

network parameters for: 
/networks/alpha_fold_networkV2_hs20_nL2_200e.pt  

and for: 
/networks/alpha_fold_networkV3_hs20_nL2_1000e.pt- 

and for: 
/networks/alpha_fold_networkV4_hs20_nL2_200e_all_prot.pt

device = 'cpu'
hidden_size = 20
num_layers = 2
dtype = 'residues'
num_classes = 1
encoding_scheme = 'onehot'
input_size = 20
problem_type = 'regression'

and for: 
/networks/alpha_fold_networkV5_hs40_nL5_200e_all_prot.pt

device = 'cpu'
hidden_size = 40
num_layers = 5
dtype = 'residues'
num_classes = 1
encoding_scheme = 'onehot'
input_size = 20
problem_type = 'regression'

for 
/networks/alpha_fold_networkV6_hs40_nL2_200e_all_prot.pt

device = 'cpu'
hidden_size = 40
num_layers = 2
dtype = 'residues'
num_classes = 1
encoding_scheme = 'onehot'
input_size = 20
problem_type = 'regression'


for 
/networks/alpha_fold_networkV7_hs100_nL2_200e_all_prot.pt

device = 'cpu'
hidden_size = 100
num_layers = 2
dtype = 'residues'
num_classes = 1
encoding_scheme = 'onehot'
input_size = 20
problem_type = 'regression'
'''


device = 'cpu'
#hidden_size = 20
# changed to 40 for v5 and v6
# changed to 100 for v7
hidden_size = 100

# 2 layers for v6, v1-4
num_layers = 2

# chaned to 5 for v5
#num_layers = 5

dtype = 'residues'
num_classes = 1
encoding_scheme = 'onehot'
input_size = 20
problem_type = 'regression'

# set location of saved_weights for load_state_dict
saved_weights = predictor

###############################################################################
# Initialize network architecture using previously defined hyperparameters
###############################################################################
brnn_network = brnn_architecture.BRNN_MtM(input_size, hidden_size, num_layers, num_classes, device).to(device)
brnn_network.load_state_dict(torch.load(saved_weights, map_location=torch.device(device)))
###############################################################################


def alpha_predict(sequence,  network=brnn_network, device=device, encoding_scheme=encoding_scheme):
    """
    The actual executing function for predicting the disorder of a sequence using metapredict.
    Returns a list containing predicted disorder values for the input sequence. 

    Arguments
    ---------
    sequence - the amino acid sequence to be predicted

    network - the network used by the predictor. See brnn_architecture BRNN_MtO for more info.

    device - String describing where the network is physically stored on the computer. 
    Should be either 'cpu' or 'cuda' (GPU).

    encoding_scheme - encoding scheme used when metapredict was trained. The encoding scheme was onehot.
    """

    # change sequence to uppercase (just in case)
    sequence = sequence.upper()

    # set seq_vector equal to converted amino acid sequence that is a PyTorch tensor of one-hot vectors
    seq_vector = encode_sequence.one_hot(sequence)
    seq_vector = seq_vector.view(1, len(seq_vector), -1)

    # get output values from the seq_vector based on the network (brnn_network)
    output = network(seq_vector.float()).detach().numpy()[0]

    # make empty list to add in outputs
    output_values = []
    # for the values 'i' in outputs
    for i in output:
        # append each value (which is the predicted disorder value) to output values as a float.
        # round each value to six digits.
        output_values.append(round(float(i), 4))

    # return the prediction
    return output_values
