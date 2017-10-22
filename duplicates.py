import hashlib
import os
import pickle
import sys


PICKLE_FILE = '/home/erikbryant/dev/duplicates/duplicates.pickle'

def get_hash(in_file):
    m = hashlib.sha256()
    m.update(open(in_file, 'rb').read())
    return m.hexdigest()


def get_files(base_dir):
    files = []

    for root, directories, filenames in os.walk(base_dir):
        for f in filenames:
            files.append(os.path.join(root, f))

    return files


def save(file_hashes):
    with open(PICKLE_FILE, 'wb') as save_file:
        pickle.dump(file_hashes, save_file)


def load():
    try:
        with open(PICKLE_FILE, 'rb') as save_file:
            return pickle.load(save_file)
    except:
        return {}


def update_hashes(base_name):
    file_hash = load()
    for f in get_files(base_name):
        if f not in file_hash.keys():
            file_hash[f] = get_hash(f)
    save(file_hash)
    return file_hash


def invert(dict1):
    dict2 = {}
    for k, v in dict1.items():
        if v not in dict2.keys():
            dict2[v] = []
        dict2[v].append(k)
    return dict2


def main(base_name):
    file_hash = update_hashes(base_name)
    hash_file = invert(file_hash)
    for h, f in hash_file.items():
        if len(f) > 1:
            print("Duplicates: %s" % f)


main(base_name=sys.argv[1])