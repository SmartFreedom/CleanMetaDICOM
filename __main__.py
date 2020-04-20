import argparse
import os
from tqdm import tqdm
import .io as io 


#  get parameters from command line
parser = argparse.ArgumentParser()

parser.add_argument(
    '--src-path',
    required=True,
    help='Source path to DICOM or MHD file or dir with DICOM files')

parser.add_argument(
    '--dst-path',
    help="""Output path to save DICOM files with cleaned personal meta.
         If parameters is not set then converted file or dir with converted
         files will be created near to source files""")

parser.add_argument(
    '--use-siuid',
    default=False, action='store_true',
    help="""Use Study Instance UID to group DICOM files.""")

parser.add_argument(
    '--postfix',
    default=False, action='store_true',
    help='Add postfix to filenames _{i}, where `i` is slice order in DICOM'
)

args = parser.parse_args()

src_path_root = args.src_path
dst_path_root = args.dst_path

print('Source path: {}'.format(src_path_root))
print('Output path: {}'.format(dst_path_root))

#  main process
dst_path_root = src_path_root if dst_path_root is None else dst_path_root

if os.path.isdir(dst_path_root):
    
    if not os.path.exists(dst_path_root):
        os.mkdir(dst_path_root)

    total_files = 0
    for root, dirs, files in os.walk(src_path_root):
        total_files += len(files)

    with tqdm(total=total_files) as pbar:
        for root, dirs, files in os.walk(src_path_root):
            for f in files:
                src_path = os.path.join(root, f)
                # print(src_path)
                try:
                    dcm = Data(src_path)
                    dst_path = root.replace(src_path_root, dst_path_root)
                    if not os.path.exists(dst_path):
                        os.makedirs(dst_path, exist_ok=True)
                    if args.use_siuid:
                        if dcm.series_uid:
                            output_filename = dcm.series_uid
                        if dcm.study_uid and args.use_siuid:
                            output_filename = dcm.study_uid
                        else:
                            output_filename = os.path.splitext(f)[0]
                    if args.postfix:
                        output_filename = '_'.join([
                            output_filename, dcm.instance_number])
                    dst_path = os.path.join(
                        dst_path, output_filename + '.png')
                    dcm.save(dst_path)
                except Exception:
                    print('{}\nFile is not DICOM or broken.'
                          .format(src_path))

                pbar.update(1)

print('Converting is finished! Have a nice day!')
