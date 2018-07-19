import hashlib
import os
import pickle
import sys

PICKLE_FILE = os.path.join(os.path.dirname(sys.argv[0]),
                           'duplicates.pickle')


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


def flush_hashes(dirname, file_hash):
    for key in list(file_hash.keys()):
        if key.startswith(dirname):
            print("Deleting: %s" % key)
            del file_hash[key]
    return file_hash


def update_hashes():
    file_hash = load()
    for i in range(1, len(sys.argv)):
        path = os.path.realpath(sys.argv[i])
        print("Flushing %s ..." % path)
        file_hash = flush_hashes(path, file_hash)
        print("Scanning %s ..." % path)
        for f in get_files(path):
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


def main():
    file_hash = update_hashes()
    hash_file = invert(file_hash)
    for h, f in hash_file.items():
        if len(f) > 1:
            print("Duplicates: %s" % f)


main()
