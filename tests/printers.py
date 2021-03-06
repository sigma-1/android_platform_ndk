#
# Copyright (C) 2015 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function

import sys

import tests.util as util


def format_stats_str(report, use_color):
    pass_label = util.color_string('PASS', 'green') if use_color else 'PASS'
    fail_label = util.color_string('FAIL', 'red') if use_color else 'FAIL'
    skip_label = util.color_string('SKIP', 'yellow') if use_color else 'SKIP'
    return '{pl} {p}/{t} {fl} {f}/{t} {sl} {s}/{t}'.format(
        pl=pass_label, p=report.num_passed,
        fl=fail_label, f=report.num_failed,
        sl=skip_label, s=report.num_skipped,
        t=report.num_tests)


class Printer(object):
    def print_result(self, result):
        raise NotImplementedError

    def print_summary(self, report):
        raise NotImplementedError


class FilePrinter(Printer):
    def __init__(self, to_file, use_color=False, show_all=False, quiet=False):
        self.file = to_file
        self.use_color = use_color
        self.show_all = show_all
        self.quiet = quiet

    def print_result(self, result):
        if self.quiet and not result.failed():
            return
        print(result.to_string(colored=self.use_color), file=self.file)

    def print_summary(self, report):
        print(file=self.file)
        formatted = format_stats_str(report, self.use_color)
        print(formatted, file=self.file)
        for suite, suite_report in report.by_suite().items():
            stats_str = format_stats_str(suite_report, self.use_color)
            print(file=self.file)
            print('{}: {}'.format(suite, stats_str), file=self.file)
            for report in suite_report.reports:
                if self.show_all or report.result.failed():
                    print(report.result.to_string(colored=self.use_color),
                          file=self.file)


class StdoutPrinter(FilePrinter):
    def __init__(self, use_color=False, show_all=False, quiet=False):
        super(StdoutPrinter, self).__init__(
            sys.stdout, use_color, show_all, quiet)
