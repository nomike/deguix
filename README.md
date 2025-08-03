# deguix

This tool filters out Guix related stuff from your environment and runs a specified command.

When you are gunning Guix on a foreign Distro (e.g. Ubuntu) and try to compile an application in that distro and not for Guix, you will often run into random segfaults due to a mashup of libraries from Guix and from the foreign distro.

To prevent this, this script gets a list of environment variable and removes

- all environment variables with "guix" in the name,
- paths with either "guix" or "/gnu/store" from a list of path like environment variables.

You just need to prefix your command with `deguix`.

For example

```shell
cmake -DEXPERIMENTAL=1 -DENABLE_PYTHON=1 -DENABLE_LIBFIVE=1  ..
```

becomes

```shell
deguix cmake -DEXPERIMENTAL=1 -DENABLE_PYTHON=1 -DENABLE_LIBFIVE=1  ..
```
