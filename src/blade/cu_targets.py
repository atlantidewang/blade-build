# Copyright (c) 2013 Tencent Inc.
# All rights reserved.
#
# Author: LI Yi <sincereli@tencent.com>
# Created:   September 27, 2013


"""
This module defines cu_library, cu_binary and cu_test rules
for cuda development.

"""

from __future__ import absolute_import

import os

from blade import build_manager
from blade import build_rules
from blade import config
from blade.blade_util import var_to_list
from blade.cc_targets import CcTarget


class CuTarget(CcTarget):
    """This class is derived from CcTarget and is the base class
    of cu_library, cu_binary etc.

    """

    def __init__(self,
                 name,
                 target_type,
                 srcs,
                 deps,
                 warning,
                 defs,
                 incs,
                 extra_cppflags,
                 extra_linkflags,
                 blade,
                 kwargs):
        srcs = var_to_list(srcs)
        deps = var_to_list(deps)
        extra_cppflags = var_to_list(extra_cppflags)
        extra_linkflags = var_to_list(extra_linkflags)

        CcTarget.__init__(self,
                          name,
                          target_type,
                          srcs,
                          deps,
                          None,
                          warning,
                          defs,
                          incs,
                          [], [],
                          extra_cppflags,
                          extra_linkflags,
                          blade,
                          kwargs)

    def _get_cu_flags(self):
        """Return the nvcc flags according to the BUILD file and other configs. """
        nvcc_flags = []

        # Warnings
        if self.data.get('warning', '') == 'no':
            nvcc_flags.append('-w')

        # Defs
        defs = self.data.get('defs', [])
        nvcc_flags += [('-D' + macro) for macro in defs]

        # Optimize flags
        if (self.blade.get_options().profile == 'release' or
                self.data.get('always_optimize')):
            nvcc_flags += self._get_optimize_flags()

        # Incs
        incs = self._get_incs_list()

        return nvcc_flags, incs


class CuLibrary(CuTarget):
    """This class is derived from CuTarget and generates the cu_library
    rules according to user options.

    """

    def __init__(self,
                 name,
                 srcs,
                 deps,
                 warning,
                 defs,
                 incs,
                 extra_cppflags,
                 extra_linkflags,
                 blade,
                 kwargs):
        CuTarget.__init__(self,
                          name,
                          'cu_library',
                          srcs,
                          deps,
                          warning,
                          defs,
                          incs,
                          extra_cppflags,
                          extra_linkflags,
                          blade,
                          kwargs)

    def ninja_rule(self):
        self.error('to be implemented')


def cu_library(name,
               srcs=[],
               deps=[],
               warning='yes',
               defs=[],
               incs=[],
               extra_cppflags=[],
               extra_linkflags=[],
               **kwargs):
    target = CuLibrary(name,
                       srcs,
                       deps,
                       warning,
                       defs,
                       incs,
                       extra_cppflags,
                       extra_linkflags,
                       build_manager.instance,
                       kwargs)
    build_manager.instance.register_target(target)


build_rules.register_function(cu_library)


class CuBinary(CuTarget):
    """This class is derived from CuTarget and generates the cu_binary
    rules according to user options.

    """

    def __init__(self,
                 name,
                 srcs,
                 deps,
                 warning,
                 defs,
                 incs,
                 extra_cppflags,
                 extra_linkflags,
                 blade,
                 kwargs):
        CuTarget.__init__(self,
                          name,
                          'cu_binary',
                          srcs,
                          deps,
                          warning,
                          defs,
                          incs,
                          extra_cppflags,
                          extra_linkflags,
                          blade,
                          kwargs)

    def ninja_rule(self):
        self.error('to be implemented')


def cu_binary(name,
              srcs=[],
              deps=[],
              warning='yes',
              defs=[],
              incs=[],
              extra_cppflags=[],
              extra_linkflags=[],
              **kwargs):
    target = CuBinary(name,
                      srcs,
                      deps,
                      warning,
                      defs,
                      incs,
                      extra_cppflags,
                      extra_linkflags,
                      build_manager.instance,
                      kwargs)
    build_manager.instance.register_target(target)


build_rules.register_function(cu_binary)


class CuTest(CuBinary):
    """This class is derived from CuBinary and generates the cu_test
    rules according to user options.

    """

    def __init__(self,
                 name,
                 srcs,
                 deps,
                 warning,
                 defs,
                 incs,
                 extra_cppflags,
                 extra_linkflags,
                 testdata,
                 always_run,
                 exclusive,
                 blade,
                 kwargs):
        # pylint: disable=too-many-locals
        CuBinary.__init__(self,
                          name,
                          srcs,
                          deps,
                          warning,
                          defs,
                          incs,
                          extra_cppflags,
                          extra_linkflags,
                          blade,
                          kwargs)
        self.type = 'cu_test'
        self.data['testdata'] = var_to_list(testdata)
        self.data['always_run'] = always_run
        self.data['exclusive'] = exclusive

        cc_test_config = config.get_section('cc_test_config')
        gtest_lib = var_to_list(cc_test_config['gtest_libs'])
        gtest_main_lib = var_to_list(cc_test_config['gtest_main_libs'])

        # Hardcode deps rule to thirdparty gtest main lib.
        self._add_hardcode_library(gtest_lib)
        self._add_hardcode_library(gtest_main_lib)


def cu_test(name,
            srcs=[],
            deps=[],
            warning='yes',
            defs=[],
            incs=[],
            extra_cppflags=[],
            extra_linkflags=[],
            testdata=[],
            always_run=False,
            exclusive=False,
            **kwargs):
    target = CuTest(name,
                    srcs,
                    deps,
                    warning,
                    defs,
                    incs,
                    extra_cppflags,
                    extra_linkflags,
                    testdata,
                    always_run,
                    exclusive,
                    build_manager.instance,
                    kwargs)
    build_manager.instance.register_target(target)


build_rules.register_function(cu_test)
