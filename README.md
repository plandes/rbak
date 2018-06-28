# Mount file systems and backup directories.

[![Travis CI Build Status][travis-badge]][travis-link]

This program copies *source* paths optionally mountable *targets*.  You can
configure whether or not a target is mountable or not.  If it is, the program
mounts the file system by looking for a `info.conf` file and mounts if the file
is not found.  The program only looks to see if this file exists and does not
do anything with the contents.

Features:

* Mounts file systems only when necessary
* Unmounts only file systems mounted
* Customizable rsync (and mount/umount) commands.
* Easy/intuitive configuration.
* Need not be `rsync`, you can customize the backup to whatever you want.


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
## Table of Contents

- [Usage](#usage)
    - [Configuration](#configuration)
    - [Help](#help)
- [Obtaining](#obtaining)
- [Changelog](#changelog)
- [License](#license)

<!-- markdown-toc end -->


## Usage

1. [Install](#obtaining) the library, which also installs the command.
2. Create a configuration file (default is `/etc/rbak.conf` if `-c` is not
   given): See the [test case configuration file] for an example.
3. Check your configuration: `$ rbak info`
4. Backup using a dry run (i.e. careful with `rsync`'s `--delete`): `$ rbak
   --dryrun backup`
5. Backup for real: `$ rbak backup`


### Configuration

See the [test case configuration file], which has the explains each line of
configuration in detail.

The `backup_cmd` need not be an `rsync` command, it can be anything
and you can use any property of the source and target that are generated at
runtime, but it can also by any property of these classes.

The global `default` section's `backup_dir` variable is shared with all targets
and sources.  This variable is appended to the target's path so the program can
differentiate between the mount point and the path to back up files.


### Help

The usage is given with `-h`:

```sql
$ rbak -h
Usage: rbak <list|...> [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -s, --short           short output for list
  -w NUMBER, --whine=NUMBER
                        add verbosity to logging
  -c FILE, --config=FILE
                        configuration file


Usage: rbak backup [additional options]

Run the backup

Options:
  -d, --dryrun  dry run to not actually connect, but act like it
  -h, --help    show this help message and exit


Usage: rbak mount [additional options]

Mount all targets

Options:
  -d, --dryrun  dry run to not actually connect, but act like it
  -h, --help    show this help message and exit


Usage: rbak umount [additional options]

Un-mount all targets

Options:
  -d, --dryrun  dry run to not actually connect, but act like it
  -h, --help    show this help message and exit
```


## Obtaining

The easist way to install the command line program is via the `pip` installer:
```bash
pip install zensols.rbak
```



## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## License

Copyright (c) 2018 Paul Landes

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


<!-- links -->
[test case configuration file]: test-resources/rbak.conf

[travis-link]: https://travis-ci.org/plandes/rbak
[travis-badge]: https://travis-ci.org/plandes/rbak.svg?branch=master
