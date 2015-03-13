#!/usr/bin/env python3
__author__ = 'otakucode'
""" autojoin - a simple utility to scan the current directory for split files and join them automatically."""
# TODO: Add neat progress indicator and verbose mode.

import argparse, os, re
from StringTool import humanize_bytes
from shutil import disk_usage


def join_files(destination, parts):
    """Concatenate the files listed in parts and output as destination."""
    try:
        with open(destination, 'wb') as dest:
            for part in parts:
                with open(part, 'rb') as p:
                    data = p.read()
                    dest.write(data)
    except:
        print("Error occurred while joining {0}.".format(destination))
        return False

    return True


def find_initial_parts(filelist):
    """Find files in filelist which are the first file in a set of split parts."""
    pattern = r'\.0+1$'
    initial_files = []
    for filename in filelist:
        ext = os.path.splitext(filename)[-1]
        if re.match(pattern, ext):
            initial_files.append(filename)
    return initial_files


def check_for_missing_parts(split_parts):
    """Check if any parts are missing from the set of split parts."""
    if len(split_parts) != int(split_parts[-1][split_parts[-1].rfind('.') + 1:]):
        return True
    return False


def find_other_parts(filelist, initial_file):
    namebase = trim_name(initial_file)
    splits = []
    for f in filelist:
        if f.startswith(namebase) and f[initial_file.rfind('.') + 1:].isnumeric():
            splits.append(f)
    splits.sort()
    return splits


def check_free_space(split_parts):
    """Checks for adequate free space to join the given set of split parts."""
    free_space = disk_usage(".").free
    needed_space = 0

    for f in split_parts:
        needed_space += os.path.getsize(f)

    return free_space >= needed_space


def trim_name(initial_file):
    return initial_file[:initial_file.rfind('.')]


def parse_args():
    parser = argparse.ArgumentParser(description='Automatically join split files.')
    parser.add_argument('--keep', '-k', action='store_true', default=False)
    parser.add_argument('--overwrite', '-o', action='store_true', default=False)
    parser.add_argument('paths', metavar='N', type=str, nargs='*',
                       help='the paths to process', default=['.'])
    args = parser.parse_args()
    return args



if __name__ == '__main__':

    the_args = parse_args()

    for p in the_args.paths:
        filelist = os.listdir(p)
        initial_parts = find_initial_parts(filelist)
        if len(initial_parts) == 0:
            print("No split files found in {0}.".format(p))
            continue

        for ip in initial_parts:
            all_parts = find_other_parts(filelist, ip)

            if len(all_parts) == 1:
                print("Found an initial part but no others.  Weird.")
                continue

            parts_with_paths = [os.path.join(p, part) for part in all_parts]

            enough_space = check_free_space(parts_with_paths)
            if not enough_space:
                print("Not enough space to join {0}".format(trim_name(ip)))
                continue

            if not the_args.overwrite and os.path.exists(trim_name(parts_with_paths[0])):
                print("Joined file {0} already detected.  Use --overwrite to overwrite file.".format(trim_name(parts_with_paths[0])))

            print("Joining {0}...".format(trim_name(parts_with_paths[0])))
            result = join_files(trim_name(parts_with_paths[0]), parts_with_paths)
            if result:   # An error occurred while joining.  Do not delete parts even if we normally should.
                if not the_args.keep:
                    # Delete the joined parts
                    for file in parts_with_paths:
                        os.unlink(file)
