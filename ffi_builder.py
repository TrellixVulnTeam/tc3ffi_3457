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
from pathlib import Path
from cffi import FFI

_tcc_build_dir = Path(__file__).resolve().parent / 'build' / 'tcc'
_tcc_lib_dir = _tcc_build_dir / 'lib'

ffi_builder = FFI()
ffi_builder.set_source(
    'tc3ffi._tcc_cffi',
    '''
    #include <libtcc.h>
    ''',
    extra_objects = [str(_tcc_lib_dir / 'libtcc.a')],
    include_dirs = [str(_tcc_build_dir / 'include')],
    extra_link_args=['-fPIC']
)
ffi_builder.cdef('''
    struct TCCState;
    typedef struct TCCState TCCState;
    TCCState *tcc_new(void);
    void tcc_delete(TCCState *s);
    void tcc_set_lib_path(TCCState *s, const char *path);
    void tcc_set_error_func(
        TCCState *s,
        void *error_opaque,
        void (*error_func)(void *opaque, const char *msg)
    );
    void tcc_set_options(TCCState *s, const char *str);
    int tcc_add_include_path(TCCState *s, const char *pathname);
    int tcc_add_sysinclude_path(TCCState *s, const char *pathname);
    void tcc_define_symbol(TCCState *s, const char *sym, const char *value);
    void tcc_undefine_symbol(TCCState *s, const char *sym);
    int tcc_add_file(TCCState *s, const char *filename);
    int tcc_compile_string(TCCState *s, const char *buf);
    int tcc_set_output_type(TCCState *s, int output_type);
    int tcc_add_library_path(TCCState *s, const char *pathname);
    int tcc_add_library(TCCState *s, const char *libraryname);
    int tcc_add_symbol(TCCState *s, const char *name, const void *val);
    int tcc_output_file(TCCState *s, const char *filename);
    int tcc_run(TCCState *s, int argc, char **argv);
    int tcc_relocate(TCCState *s1, void *ptr);
    void *tcc_get_symbol(TCCState *s, const char *name);
    
    #define TCC_OUTPUT_MEMORY   1
    #define TCC_OUTPUT_EXE      2
    #define TCC_OUTPUT_DLL      3
    #define TCC_OUTPUT_OBJ      4
    #define TCC_OUTPUT_PREPROCESS 5
''')

if __name__ == '__main__':
    ffi_builder.compile(verbose=True)

