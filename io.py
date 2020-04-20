import pydicom as dicom
import numpy as np
import SimpleITK as sitk
import os


import pydicom as dicom
import numpy as np
import cv2


EMPTY_VALUE = '*' * 30


class Data:

    def __init__(self, dcm_path):
        """Convert DICOM file to PNG
        This class can be used to clean personal meta data from DICOM or MHD file.
        Parameters:
        -----------
            dcm_path - str;
                path to raw DICOM or MHD file
        """

        try:
            self.dcm = read(dcm_path)
            self.dcm = self.clean_meta(self.dcm)
        except Exception:
            print('File "{}" is not DICOM or broken'.format(dcm_path))
            self.dcm = None
            return None

        #  get study uid
        self.study_uid = self.dcm.get('StudyInstanceUID')
        if self.study_uid:
            self.study_uid = self.study_uid.replace('.', '_')

        #  get series name
        self.series_uid = self.dcm.get('SeriesInstanceUID')
        if self.series_uid:
            self.series_uid = self.series_uid.replace('.', '_')

    def save(self, output_path):
        if self.dcm is None:
            return False

        dcm.save_as(output_path)
        return True


def clean_meta(dcm):
    dcm.add(dicom.DataElement((0x0008, 0x0023), 'DA', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0008, 0x0033), 'TM', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0008, 0x1050), 'PN', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0008, 0x1070), 'PN', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x0030), 'DA', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x1000), 'LO', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x1040), 'LO', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x2154), 'SH', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x2160), 'SH', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x2180), 'SH', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x21b0), 'LT', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0010, 0x21f0), 'LO', EMPTY_VALUE))
    dcm.add(dicom.DataElement((0x0038, 0x0500), 'LO', EMPTY_VALUE))

    return dcm


def read(path: str, verbose=False):
    # Read the slices from the dicom or MHD directory or file
    slices = []
    if os.path.isfile(path):
        try:
            return sitk.ReadImage(path)
        except:
            try:
                return dicom.read_file(path)
            except:
                if verbose: 
                    print(
                        'Neither a DICOM nor a MHD file: {}'.format(
                            os.path.basename(path)))

    if os.path.isdir(path):
        files = os.listdir(path)
        for filename in files:
            try:
                slices.append(dicom.read_file(os.path.join(path, filename)))
            except dicom.filereader.InvalidDicomError:
                if verbose:
                    print('Neither a DICOM nor a MHD file: {}'.format(filename))

        try:
            slices.sort(key=lambda x: int(x.InstanceNumber))
        except:
            if verbose:
                    print('No InstanceNumber has been found')

        return slices
