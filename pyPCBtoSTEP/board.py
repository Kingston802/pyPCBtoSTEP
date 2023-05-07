import os
import solid as s

from .util import copper_weight_to_thickness


class Board:
    """
        Represents board containing gerber files 
    """

    def __init__(self, directory, verbose=False):
        # kwargs
        self.directory = directory
        self.verbose = verbose

        self.files = {}

    def get_files(self):
        return self.files

    def open_files(self):
        self.files['drill'] = ''
        self.files['outline'] = ''
        self.files['top_copper'] = ''
        self.files['top_mask'] = ''
        self.files['top_silk'] = ''
        self.files['bottom_copper'] = ''
        self.files['bottom_mask'] = ''
        self.files['bottom_silk'] = ''

        # RS274X name schemes
        unidentified_files = 0
        for root, dirs, files in os.walk(self.directory):
            for filename in files:
                if (not self.files['drill'] and filename[-3:].upper() == 'DRL' or filename[-3:].upper() == 'XLN'):
                    self.files['drill'] = open(root+'/'+filename, 'r').read()
                elif (not self.files['outline'] and (filename[-3:].upper() == 'GKO' or filename[-3:].upper() == 'GM1')):
                    self.files['outline'] = open(root+'/'+filename, 'r').read()
                elif (not self.files['top_copper'] and filename[-3:].upper() == 'GTL'):
                    self.files['top_copper'] = open(
                        root+'/'+filename, 'r').read()
                elif (not self.files['top_mask'] and filename[-3:].upper() == 'GTS'):
                    self.files['top_mask'] = open(
                        root+'/'+filename, 'r').read()
                elif (not self.files['top_silk'] and filename[-3:].upper() == 'GTO'):
                    self.files['top_silk'] = open(
                        root+'/'+filename, 'r').read()
                elif (not self.files['bottom_copper'] and filename[-3:].upper() == 'GBL'):
                    self.files['bottom_copper'] = open(
                        root+'/'+filename, 'r').read()
                elif (not self.files['bottom_mask'] and filename[-3:].upper() == 'GBS'):
                    self.files['bottom_mask'] = open(
                        root+'/'+filename, 'r').read()
                elif (not self.files['bottom_silk'] and filename[-3:].upper() == 'GBO'):
                    self.files['bottom_silk'] = open(
                        root+'/'+filename, 'r').read()
                elif (filename[-3:].upper() == 'GBR'):
                    temp = open(root+'/'+filename, 'r').read()
                    self.infer_filetype(temp, filename)
                else:
                    unidentified_files += 1

        if unidentified_files:
            print(f'{unidentified_files} files are unidentified')

        print(self.files)

    def infer_filetype(self, file, filename):
        upper_file = file.upper()
        if ('PROFILE' in filename[:-4].upper() or 'OUTLINE' in filename[:-4].upper()):
            self.files['outline'] = file
        elif ('DRILL' in filename[:-4].upper() or 'DRILL' in filename[:-4].upper()):
            self.files['drill'] = file
        elif ('TOP' in filename[:-4].upper() or upper_file.find('TOP') != -1):
            if ('COPPER' in filename[:-4].upper() or upper_file.find('COPPER') != -1):
                self.files['top_copper'] = file
            elif ('MASK' in filename[:-4].upper() or upper_file.find('MASK') != -1):
                self.files['top_mask'] = file
            elif ('LEGEND' in filename[:-4].upper() or 'SILK' in filename[:-4].upper() or upper_file.find('LEGEND') != -1 or upper_file.find('SILK') != -1):
                self.files['top_silk'] = file
        elif ('BOT' in filename[:-4].upper() or upper_file.find('BOT') != -1):
            if ('COPPER' in filename[:-4].upper() or upper_file.find('COPPER') != -1):
                self.files['bottom_copper'] = file
            elif ('MASK' in filename[:-4].upper() or upper_file.find('MASK') != -1):
                self.files['bottom_mask'] = file
            elif ('LEGEND' in filename[:-4].upper() or 'SILK' in filename[:-4].upper() or upper_file.find('LEGEND') != -1 or upper_file.find('SILK') != -1):
                self.files['bottom_silk'] = file

    def draw_copper(self, copper_weight):
        thickness = copper_weight_to_thickness(copper_weight)

        obj = s.cube((1, 1, thickness))

        print(s.scad_render(obj))
