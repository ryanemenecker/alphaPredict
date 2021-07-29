##
## alpha.py
## 
## alpha.py contains all the user-facing function associated with alphaPredict. 
## If a new function is added it should be included
## here and added to the __all__ list
## 

##Handles the primary functions


__all__ =  ['predict', 'graph']
 
import os
import sys

# note - we imort packages below with a leading _ which means they are ignored in the import

#import protfasta to read .fasta files
import protfasta as _protfasta

# import stuff for IDR predictor from backend. Note the 'as _*' hides the imported
# module from the user
#from predictAlpha.backend.parrot_alpha import alpha_predict as _alpha_predict
from alphaPredict.backend.parrot_alpha import alpha_predict as _alpha_predict
from alphaPredict.backend import alpha_tools as _alpha_tools
from alphaPredict.backend.alpha_graph import graph as _graph
# stuff for uniprot from backend
from alphaPredict.alpha_exceptions import AlphaError



def predict(sequence):
    """
    Function to return confidence scores from
    Alpha fold 2 of a single input sequence. Returns the
    predicted values as a float.

    Parameters
    ------------

    sequence : str 
        Input amino acid sequence (as string) to be predicted.

    Returns
    --------
    
    Float
        Returns a float of the confidence score value (predicted)

    """
    # make all residues upper case 
    sequence = sequence.upper()

    # return predicted values of disorder for sequence
    return _alpha_predict(sequence)


def graph(sequence,
          title='Predicted Confidence Score',
          confidence_threshold=50,
          shaded_regions=None,
          shaded_region_color='red',
          confidence_line_color='blue',
          threshold_line_color='black',
          DPI=150,
          output_file=None):
    _graph(sequence, title, confidence_threshold, 
            shaded_regions, shaded_region_color,
            confidence_line_color, threshold_line_color,
            DPI, output_file)
    
    
