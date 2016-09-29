###########################
# POSTPROCESSING // UNZIP #
###########################

# py_wah.unzip_wah('/net/exo/landclim/mathause/EUCLEIA/w_at_h/hadam3p_eu', '*_7.zip');
# py_wah.unzip_wah('/net/exo/landclim/mathause/EUCLEIA/w_at_h/hadam3p_eu', '*_8.zip');
# py_wah.unzip_wah('/net/exo/landclim/mathause/EUCLEIA/w_at_h/hadam3p_eu', '*_9.zip');

# py_wah.unzip_wah('/net/exo/landclim/mathause/EUCLEIA/w_at_h/hadam3p_eu_2014', '*_8.zip');
# py_wah.unzip_wah('/net/exo/landclim/mathause/EUCLEIA/w_at_h/hadam3p_eu_2014', '*_9.zip'); 

import os
import glob
from subprocess import call

def unzip(folder, pattern='*.zip', file_pattern='*ga.pe*'):
    """
    unzip weather at home simulations

    Parameters
    ----------
    folder : string
        Path to folder.
    pattern : string
        Wildcard string to pass to glob. Default '*.zip'.
    file_pattern : string
        Filename pattern to extract. Default: '*ga.pe*' (regional
        monthly). Others: '*ga.pd*' (regional daily) '*ma.pc*'
        (global monthly)

    Example
    -------
    # unzip_wah('/path/w_at_h/hadam3p_eu_2014', '*_7.zip', '*ga.pe*');



    """

    if file_pattern not in ('*ga.pe*', '*ga.pd*', '*ma.pc*'):
        raise AssertionError('invalid file pattern')

    # list all files in 
    glob_pattern = path.join(folder, pattern)

    # the file pattern must be enclosed in single apostroph
    file_pattern = "'{}'".format(file_pattern)

    fNs = glob.glob(glob_pattern)

    for fN in fNs:
        _unzip_wah_one_file(fN, file_pattern)


def _unzip_wah_one_file(zipfile, file_pattern):

    # is equivalent to the following bash command
    # unzip hadam3p_eu_faqn_2013_1_010205811_0_9.zip '*ga.pe*' -d hadam3p_eu_faqn_2013_1_010205811_0_9

    dest_folder = path.splitext(zipfile)[0]
    cmd = ' '.join(['unzip', '-n', zipfile, file_pattern, '-d', dest_folder])
    #call(['unzip', zipfile, file_pattern, '-d', dest_folder], shell=True)
    call(cmd, shell=True)