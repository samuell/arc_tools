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
            item = bits[0]
            type = bits[1]
            if type == "dir":
                subdir_to_remove = "%s/%s" % (dir_to_remove, item)
                print "INFO: Navigating down in subdir: %s" % subdir_to_remove
                remove_recursively(subdir_to_remove)
            elif type == "file":
                filepath = os.path.join(dir_to_remove, item)
                # Don't duplicate logging
                # print "INFO: Removing file: %s" % filepath
                exec_command(["ngrm", filepath])
        else:
            print "INFO: No more subfolders here, so deleting folder: " + dir_to_remove
            output = exec_command(["ngrm", dir_to_remove])
            print "INFO: Output: " + output

# ----------------------------------------------------------------------------
#   Main Loop
# ----------------------------------------------------------------------------

if dir_to_remove is None:
    print "No directory specified. use the -h flag to view options"
else:
    remove_recursively(dir_to_remove)

