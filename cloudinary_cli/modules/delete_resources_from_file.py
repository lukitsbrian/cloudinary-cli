from click import command, argument, option
from cloudinary import api
from cloudinary.utils import cloudinary_url as cld_url
from os import getcwd, walk, sep, remove, rmdir, listdir, mkdir
from os.path import dirname, splitext, split, join as path_join, abspath, isdir
from requests import get, head
from hashlib import md5
from itertools import product
from functools import reduce
from threading import Thread, active_count
from time import sleep
from ..utils import parse_option_value, log, F_OK, F_WARN, F_FAIL, load_template
from ..defaults import TEMPLATE_EXTS
from queue import Queue

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

@command("delete_resources_from_file")
@argument("path", nargs=1)
@option("-rt", "--resource_type", nargs=1, default="image")
@option("-t", "--type", nargs=1, default="upload")
@option("-I", "--invalidate", is_flag=True)
def delete_resources_from_file(path, resource_type, type, invalidate):

    with open(path, "r") as f:
        resources_to_delete = f.read().split("\n")
    
    gen = chunks(resources_to_delete, 100)
    op_number = 0

    threads = []
    output_log_file = path_join(getcwd(),"delete_resources_from_file.log")
    while True:
        try:
            chunk = next(gen)
        except StopIteration:
            break

        res = api.delete_resources(chunk, resource_type=resource_type, type=type, invalidate=invalidate)
        open(output_log_file, "a").write(str(res) + "\n")
        print("Chunk {} done".format(op_number))
        op_number += 1
