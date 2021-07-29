
import re
from alphaPredict.alpha_exceptions import AlphaError



def write_csv(input_dict, output_file):
    """
    Function that writes the scores in an input dictionary out to a standardized CVS file format.

    Parameters
    -----------
    input_dict : dict
        Dictionary where keys are headers/identifiers and values is a list of per-residue
        disorder score

    output_file : str
        Location and filename for the output file. Assumes .csv is provided.

    Returns
    --------
    None
        No return value, but writes a .csv file to disk


    """

    # try and open the file and throw exception if anything goes wrong
    try:
        fh = open(output_file, 'w')
    except Exception:
        raise AlphaError('Unable to write to file destination %s' % (output_file))

    # for each entry
    for idx in input_dict:

        # important otherwise commmas in FASTA headers render the CSV file unreadable!
        no_comma = idx.replace(',', ' ')
        fh.write('%s' % (no_comma))

        # for each score write
        for score in input_dict[idx]:
            fh.write(', %1.3f' % (score))
        fh.write('\n')
