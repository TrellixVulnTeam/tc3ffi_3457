# Copyright (c) 2020, Slavfox
#
# This file is part of tc3ffi.
#
# tc3ffi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 2 of
# the License, or (at your option) any later version.
#
# tc3ffi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with tc3ffi.  If not, see
# <https://www.gnu.org/licenses/>.
from subprocess import run
import sys
from shutil import rmtree
import tarfile
from pathlib import Path
from urllib.request import urlretrieve, urlcleanup

import colorama as c

UTILS_DIR: Path = Path(__file__).resolve().parent
BASE_DIR: Path = UTILS_DIR.parent
BUILD_DIR: Path = BASE_DIR / 'build'
TCC_BUILD_DIR: Path = BUILD_DIR / 'tcc'

TCC_VERSION = '0.9.27'
WINDOWS = sys.platform == 'win32'
if WINDOWS:
    if sys.maxsize > 2**32:
        TCC_EXT = '-win64-bin.zip'
    else:
        TCC_EXT = '-win32-bin.zip'
else:
    TCC_EXT = '.tar.bz2'

TCC_FILENAME = f'tcc-{TCC_VERSION}{TCC_EXT}'
TCC_URL = f'https://download.savannah.gnu.org/releases/tinycc/{TCC_FILENAME}'

def _info(msg):
    print(f"{c.Fore.BLUE}[info]{c.Style.RESET_ALL} {msg}")
def _success(msg):
    print(f"{c.Style.BRIGHT}{c.Fore.GREEN}[success]{c.Style.RESET_ALL} {msg}")

c.init()

def get_tcc(cleanup=True):
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    try:
        if WINDOWS:
            _get_tcc_windows()
        else:
            _get_tcc_good_os(cleanup)
    finally:
        _info(f"Cleaning up downloaded temporary files.")
        urlcleanup()

def _get_tcc_good_os(cleanup=True):
    _info(f"Fetching TCC sources.")
    filename, _ = urlretrieve(TCC_URL)
    _info(f"TCC sources saved to {filename}.")
    with tarfile.open(filename) as srctar:
        tcc_src_dir = BUILD_DIR / srctar.firstmember.path
        _info(f"Extracting TCC sources.")
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(srctar, BUILD_DIR)
        _info(f"TCC sources extracted to {BUILD_DIR}.")
    _info(f"Configuring build.")
    run(
        ["./configure", f"--prefix={TCC_BUILD_DIR}", f"--extra-cflags=-fPIC"],
        cwd=tcc_src_dir,
        check=True
    )
    _info(f"Building TCC.")
    run(
        ["make", "-j4"],
        cwd=tcc_src_dir,
        check=True
    )
    run(
        ["make", "install"],
        cwd=tcc_src_dir,
        check=True
    )
    _success(f"Built TCC.")
    if not cleanup:
        return
    _info(f"Removing build files.")
    rmtree(str(tcc_src_dir))


def _get_tcc_windows():
    # ToDo
    raise WindowsError("Get a better operating system")


if __name__ == "__main__":
    cleanup = sys.argv[1:2] != ['--no-cleanup']
    get_tcc(cleanup)
