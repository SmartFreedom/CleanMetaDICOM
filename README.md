# CleanMetaDICOM
Clean DICOM personal meta information

```
usage: CleanMeta [-h] --src-path SRC_PATH [--dst-path DST_PATH] [--use-siuid]

optional arguments:
  -h, --help           show this help message and exit
  --src-path SRC_PATH  Source path to DICOM or MHD file or dir with DICOM
                       files
  --dst-path DST_PATH  Output path to save DICOM files with cleaned personal
                       meta. If parameters is not set then converted file or
                       dir with converted files will be created near to source
                       files
  --use-siuid          Use Study Instance UID to group DICOM files.
```
