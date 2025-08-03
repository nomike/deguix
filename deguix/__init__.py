#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of dequix.
#
# deuix is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at
# your option) any later version.
#
# deguix is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deguix.  If not, see <http://www.gnu.org/licenses/>.

"""
deguix - Run commands without Guix environment variables

Usage:
    deguix <command> [<args>...]
"""

import os
import subprocess
import sys


def is_path_var(var_name):
    # Common path-like variables
    path_vars = {
        "PATH",
        "LD_LIBRARY_PATH",
        "PYTHONPATH",
        "MANPATH",
        "PKG_CONFIG_PATH",
        "XDG_DATA_DIRS",
        "GIO_EXTRA_MODULES",
    }
    return var_name.upper().endswith("PATH") or var_name in path_vars


def filter_env(env):
    new_env = {}
    for k, v in env.items():
        if "GUIX" in k.upper():
            continue
        if is_path_var(k):
            paths = v.split(":")
            filtered = []
            for p in paths:
                if "guix" in p.lower() or "/gnu/store" in p.lower():
                    continue
                filtered.append(p)
            new_env[k] = ":".join(filtered)
        else:
            new_env[k] = v
    return new_env


def main():
    filtered_env = filter_env(os.environ)

    try:
        result = subprocess.run(sys.argv[1:], env=filtered_env)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("Command not found.", file=sys.stderr)
        sys.exit(127)
    except Exception as e:
        print(f"Error running command: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
