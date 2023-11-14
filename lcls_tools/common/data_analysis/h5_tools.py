import os
from typing import Optional
import h5py
import numpy as np


def _check_file(path_to_file: str = ""):
    return os.path.exists(path_to_file)


def _construct_dataset_as_dictionary(
    file_obj: h5py.File,
    dataset_name: str,
    with_metadata: Optional[bool] = True,
    average_over_dataset: Optional[bool] = False,
):
    dset_dict = {
        dataset_name: {"dataset": {}, "metadata": {}},
    }
    if not with_metadata:
        dset_dict = {dataset_name: {"dataset": {}}}
    data = file_obj[:][:]
    metadata = file_obj.attrs
    dset_dict[dataset_name]["dataset"] = data
    dset_dict[dataset_name]["metadata"].update(metadata)
    return dset_dict



def get_datasets_from_file(
    filename: str,
    with_metadata: Optional[bool] = True,
    average_over_dataset: Optional[bool] = False,
):
    """Assumes that datasets contain 2-D array"""
    if _check_file(filename):
        datasets = {}
        with h5py.File(filename, "r") as f:
            [
                datasets.update(
                    _construct_dataset_as_dictionary(
                        file_obj=f[dset_name],
                        dataset_name=dset_name,
                        with_metadata=with_metadata,
                    )
                )
                for dset_name in f
            ]
        return datasets
    else:
        print(f"could not find {filename}")
