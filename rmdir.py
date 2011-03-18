#!/usr/bin/python

# @author Samuel Lampa <samuel.lampa@gmail.com>
# @summary Convenience script to recursively delete directories via the 
#          ARC SRM Client

import subprocess, string, os
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--directory", dest="dir_to_remove", type="string",
                  help="Full path to directory to remove, including 'srm://' and the domain name")
(options, args) = parser.parse_args()
dir_to_remove = options.dir_to_remove

# ----------------------------------------------------------------------------
#   Functions
# ----------------------------------------------------------------------------

def exec_command(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    output = string.strip(output)
    return output

def remove_recursively(dir_to_remove):
    output = exec_command(["ngls", "-r", "0", "-l", dir_to_remove])
    lines = string.split(output, "\n")
    for line in lines:
        if line is not "":
            bits = line.split(" ")
            if len(bits) > 1:
                item = bits[0]
                type = bits[1]
                item_path = os.path.join(dir_to_remove, item)
                if type == "dir":
                    print("Navigating down in subdir: %s" % item_path)
                    remove_recursively(item_path)
                elif type == "file":
                    # print "Removing file: %s" % filepath
                    exec_command(["ngrm", item_path])
    print("No more subfolders here, so deleting folder: %s" % dir_to_remove)
    exec_command(["ngrm", dir_to_remove])

# ----------------------------------------------------------------------------
#   Main Loop
# ----------------------------------------------------------------------------

if dir_to_remove is None:
    print("No directory specified. Use the -h flag to view options")
else:
    remove_recursively(dir_to_remove)

