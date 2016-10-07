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
import contextlib
import logging
import os
import subprocess


def logger():
    """Returns the logger for this module."""
    return logging.getLogger(__name__)


def color_string(string, color):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
    }
    end_color = '\033[0m'
    return colors[color] + string + end_color


def maybe_color(text, color, do_color):
    return color_string(text, color) if do_color else text


@contextlib.contextmanager
def cd(path):
    curdir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(curdir)


def _call_output_inner(cmd, *args, **kwargs):
    """Does the real work of call_output.

    This inner function does the real work and the outer function handles the
    OS specific stuff (Windows needs to handle WindowsError, but that isn't
    defined on non-Windows systems).
    """
    logger().info('Popen: %s', ' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, *args, **kwargs)
    out, _ = proc.communicate()
    return proc.returncode, out


def call_output(cmd, *args, **kwargs):
    """Invoke the specified command and return exit code and output.

    This is the missing subprocess.call_output, which is the combination of
    subprocess.call and subprocess.check_output. Like call, it returns an exit
    code rather than raising an exception. Like check_output, it returns the
    output of the program. Unlike check_output, it returns the output even on
    failure.

    Returns: Tuple of (exit_code, output).
    """
    if os.name == 'nt':
        try:
            return _call_output_inner(cmd, *args, **kwargs)
        except WindowsError as error:  # pylint: disable=undefined-variable
            return error.winerror, error.strerror
    else:
        return _call_output_inner(cmd, *args, **kwargs)
