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
from abc import ABC
from enum import Enum
from typing import List, Any

from tc3ffi._tcc_cffi import lib as _lib, ffi as _ffi

class OutputType(Enum):
    MEMORY = _lib.TCC_OUTPUT_MEMORY
    EXE = _lib.TCC_OUTPUT_EXE
    DLL = _lib.TCC_OUTPUT_DLL
    OBJ = _lib.TCC_OUTPUT_OBJ
    PREPROCESS = _lib.TCC_OUTPUT_PREPROCESS

class TccExecutor(ABC):
    def __init__(self):
        self._tcc = _lib.tcc_new()

    def _set_output_type(self, t: OutputType):
        _lib.tcc_set_output_type(self._tcc, t.value)

    def compile(self, s: str):
        if not isinstance(s, bytes):
            s = s.encode()
        _lib.tcc_compile_string(self._tcc, s)

class TccRunner(TccExecutor):
    def __init__(self):
        super().__init__()
        self._set_output_type(OutputType.MEMORY)

    def run(self, *args: List[Any]):
        return _lib.tcc_run(self._tcc, len(args), args)



