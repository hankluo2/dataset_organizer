from pathlib import Path
import shutil
import random


def split_train_val_set(data_root_dir: str,
                        file_format: str,
                        ratio: float,
                        shuffle=False):
    output_dir = 'splitted_' + data_root_dir
    # find classes and get information
    class2imageset = {}  # Dict[class]: file_path
    for node in Path(data_root_dir).glob("*"):
        if node.is_dir():
            class2imageset[node.stem] = []
            # custom a searching logic to get
            for item in node.rglob(f"*.{file_format}"):
                class2imageset[node.stem].append(item)

    # sort lists of each class
    for key in class2imageset:
        class2imageset[key] = sorted(class2imageset[key])

    if shuffle:
        for key in class2imageset:
            class2imageset[key] = random.shuffle(class2imageset[key])

    # split dataset
    trainset, valset = {}, {}
    for klass in class2imageset:
        offset = int(ratio * len(class2imageset[klass]))
        trainset[klass] = class2imageset[klass][:offset]
        valset[klass] = class2imageset[klass][offset:]
        # print(len(trainset[klass]), len(valset[klass]))

    # Move to a new directory
    """
    output_dir/train/xxx.png
    output_dir/train/xxy.png
    ...
    output_dir/train/zzz.png
    """
    phase2set = {'train': trainset, 'val': valset}
    for phase in ['train', 'val']:
        for klass in phase2set[phase]:
            cp_dir = Path(output_dir) / phase / klass
            # cp_dir.mkdir(parents=True, exist_ok=True)  # TODO: test only
            cp_dir.mkdir(parents=True, exist_ok=False)

            src_paths = phase2set[phase][klass]
            for src_path in src_paths:
                dest_path = cp_dir / src_path.name
                print(src_path, dest_path)
                shutil.copy(src_path, dest_path)


if __name__ == "__main__":
    data_root_dir = 'chss_dataset'
    ratio = 0.8
    split_train_val_set(data_root_dir, 'jpg', ratio)
