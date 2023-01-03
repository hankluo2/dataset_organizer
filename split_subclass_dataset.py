from pathlib import Path
import shutil
import random


def split_subclass_dataset(root_dir: str, dest_dir: str, split_ratio: float):
    """Find the subclass folders in a dataset structured as follows::
        root_dir/
        ├── class_x
        │   ├── sub_class_x
        │   ├── sub_class_y
        │   └── ...
        │       └── file1.format
        │       └── file2.format
        │       └── ...
        ├── class_y
            ├── sub_class_x
            ├── sub_class_y
            └── ...
                └── file1.format
                └── file2.format
                └── ...
    """
    for klass in Path(root_dir).glob("*"):
        for sub_klass in klass.glob("*"):
            group_files = list(sub_klass.glob("*"))
            random.shuffle(group_files)

            train_files = group_files[:int(split_ratio * len(group_files))]
            test_files = group_files[int(split_ratio * len(group_files)):]

            train_dir = Path(dest_dir) / 'train' / klass.name / sub_klass.name
            test_dir = Path(dest_dir) / 'test' / klass.name / sub_klass.name
            train_dir.mkdir(parents=True, exist_ok=True)
            test_dir.mkdir(parents=True, exist_ok=True)

            for file in train_files:
                shutil.copy(file, train_dir / file.name)
            for file in test_files:
                shutil.copy(file, test_dir / file.name)
