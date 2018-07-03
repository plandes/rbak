import logging
import os

from zensols.rbak import Executor

logger = logging.getLogger('zensols.rbak.target')


class Target(object):
    """Represents to where files are backed up.  Sometimes this is an external
    file system.
    """
    def __init__(self, name, executor, config):
        self.name = name
        self.executor = executor
        conf = {'name': name}
        conf.update(config.get_options('default'))
        conf.update(config.get_options(name))
        self.info_file = conf['info_file']
        self.mountable = config.get_option_boolean('mountable', name, expect=True)
        mp_fmt = config.get_option('path', name, expect=True)
        self.path = mp_fmt.format(**conf)
        conf['path'] = self.path
        self.mount_cmd = conf['mount_cmd'].format(**conf)
        self.umount_cmd = conf['umount_cmd'].format(**conf)
        self.backup_dir = conf['backup_dir']

    @property
    def info_path(self):
        """Return the path of the `info.conf` file to determine if this target is
        mounted.
        """
        return os.path.join(self.path, self.info_file)

    @property
    def backup_path(self):
        "Return the path of where the target directory."
        if len(self.backup_dir) > 0:
            return os.path.join(self.path, self.backup_dir)
        else:
            return self.path

    @property
    def is_mounted(self):
        "Return whether or not this target is an external mountable path."
        return os.path.isfile(self.info_path)

    def _assert_mountable(self):
        "Raise an error if this target is mountable."
        if not self.mountable:
            raise ValueError('target {} is not mountable'.format(self))

    def mount(self):
        "Mount the target if not already.  Raise error if it is not mountable."
        self._assert_mountable()
        if  self.is_mounted:
            logger.warning('{} is already mounted'.format(self.path))
        else:
            logger.info('mounting {}'.format(self))
            self.executor.run(self.mount_cmd)

    def umount(self):
        "Unmount the target if not already.  Raise error if it is not mountable."
        self._assert_mountable()
        if not self.is_mounted:
            logger.warning('{} is not mounted'.format(self.path))
        else:
            logger.info('un-mounting {}'.format(self))
            self.executor.run(self.umount_cmd)

    def __str__(self):
        mnt_str = ', mounted={}'.format(self.is_mounted) if self.mountable else ''
        return '{} on {}{}'.format(self.name, self.path, mnt_str)

    def __repr__(self):
        return self.__str__()


class Source(object):
    """
    Represents from where files are backed up.
    """
    def __init__(self, name, config):
        self.name = name
        self.path = config.get_option('path', name, expect=True)
        self.basename_dir = config.get_option('basename_dir', name)

    @property
    def basename(self):
        "Return the basename (sans file name) of the source path."
        return self.basename_dir or os.path.basename(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.__str__()
