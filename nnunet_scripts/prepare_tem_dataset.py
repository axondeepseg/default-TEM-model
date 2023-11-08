#!/usr/bin/env python3
"""Prepares the TEM data for nnUNetv2 training
The 2 output classes must be put in a single mask with values 1 and 2
(0 is for background). All subjects with annotations are put in the 
training set (nnUNet will do cross-validation automatically), except for 
`sub-nyuMouse26` which is excluded for model evaluation.
"""

__author__ = "Armand Collin"
__license__ = "MIT"

import argparse
import json
import cv2
import numpy as np
from pathlib import Path


def main(args):
    datapath = Path(args.DATAPATH)
    derivatives = list((datapath / 'derivatives' / 'labels').glob('sub*'))
    subject_list = [d.name for d in derivatives]
    # create nnUNet_raw folder
    out_folder = Path.cwd() / 'nnUNet_raw' / 'Dataset002_TEM'
    out_folder.mkdir(parents=True, exist_ok=True)
    (out_folder / 'imagesTr').mkdir(exist_ok=True)
    (out_folder / 'labelsTr').mkdir(exist_ok=True)
    (out_folder / 'imagesTs').mkdir(exist_ok=True)
    # create dataset.json
    dataset_info = {
        "channel_names": {
            "0": "rescale_to_0_1"
        },
        "labels": {
            "background": 0,
            "myelin": 1, 
            "axon": 2 
        },
        "numTraining": 150,
        "file_ending": ".png"
    }
    with open('nnUNet_raw/Dataset002_TEM/dataset.json', 'w') as f:
        f.write(json.dumps(dataset_info, indent=1))

    # save correspondence between original fnames and case IDs
    case_id_dict = {}
    case_id = 1
    test_subj = 'sub-nyuMouse26'

    # put images in imagesTr
    for subject in subject_list:

        if subject == test_subj:
            # skip test subject
            continue

        subj_files = (datapath / subject / 'micr').glob('*.png')
        for img_fname in subj_files:
            img = cv2.imread(str(img_fname))
            fname = f'VCU_{case_id:03d}_0000.png'
            cv2.imwrite(str(out_folder / 'imagesTr' / fname), img)
        
            # put labels in labelsTr
            basename = f'{img_fname.stem}_seg-'
            ax_path = datapath / 'derivatives' / 'labels' / subject / 'micr' / f'{basename}axon-manual.png'
            my_path = datapath / 'derivatives' / 'labels' / subject / 'micr' / f'{basename}myelin-manual.png'
            ax = cv2.imread(str(ax_path)) // 255
            my = cv2.imread(str(my_path)) // 255
            label = my + 2 * ax
            fname = f'VCU_{case_id:03d}.png'
            #NOTE: might need to only take one channel for the GT?
            cv2.imwrite(str(out_folder / 'labelsTr' / fname), label)
            
            # log and increment case_id
            case_id_dict[str(case_id)] = img_fname
            case_id += 1

    # put test subject images in imagesTs
    test_case_id = max(case_id_dict.keys()) + 1
    for img_fname in (datapath / test_subj / 'micr').glob('*.png'):
        img = cv2.imread(str(img_fname))
        fname = f'VCU_{test_case_id:03d}_0000.png'
        cv2.imwrite(str(out_folder / 'imagesTs' / fname), img)
        
        # add the test subject to case_id_dict
        case_id_dict[test_case_id] = img_fname
        test_case_id += 1
    
    with open('subject_to_case_identifier.json', 'w') as f:
        f.write(json.dumps(case_id_dict, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("DATAPATH", help="path to TEM dataset (BIDS format)")
    # Optional argument flag which defaults to False
    parser.add_argument(
        "-m", "--move", 
        action="store_true", 
        default=False,
        help='move files instead of copying them')

    args = parser.parse_args()
    main(args)