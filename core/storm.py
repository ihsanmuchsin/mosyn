"""
STORM Function
"""


import os
import subprocess
import glob

import prep.fasta as pf

from misc.string import check_folder_path


def get_base_composition(infile):
    """
    Get the base composition from FASTA file
    :param infile: Genomic FASTA file
    :return: String of base composition
    """

    return str(subprocess.check_output(['basecomp', infile]))[2:-1]


def run_storm(infolder, pwm_folder, outfolder, storm_options=None, calculate_base_comp=False):
    """
    Run CREAD STORM
    :param infolder: Folder containing genome files in .fasta format
    :param pwm_folder: Folder containing position weight matrices files in TRANSFAC format
    :param outfolder: Output folder
    :param storm_options: String of orthofinder options
    :param calculate_base_comp: Calculate base composition
    :return:
    """

    infolder = check_folder_path(infolder)
    pwm_folder = check_folder_path(pwm_folder)
    outfolder = check_folder_path(outfolder, True)

    working_directory = outfolder + 'working_directory/'
    working_directory = check_folder_path(working_directory, True)

    cleaned_fasta = working_directory + 'cleaned_fasta/'
    cleaned_fasta = check_folder_path(cleaned_fasta, True)

    pf.clean_header_fasta_folder(infolder, cleaned_fasta)

    for fas in glob.glob(cleaned_fasta + '*'):

        acgt = None

        if calculate_base_comp:
            acgt = '--base-comp=' + get_base_composition(fas)

        for pwm in glob.glob(pwm_folder + '*'):

            sub_outfolder = outfolder + os.path.basename(pwm).split('.')[0]
            sub_outfolder = check_folder_path(sub_outfolder, True)

            outfile = sub_outfolder + os.path.basename(fas).split('.')[0] + '.storm'

            list_command = ['storm', '-s', fas, pwm, '-o', outfile]

            if acgt:
                list_command.append(acgt)

            if storm_options:
                list_opt = storm_options.split(' ')
                list_command += list_opt

            subprocess.call(list_command)
