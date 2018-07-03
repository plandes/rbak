import os
import pathlib
import sys
import logging

from zensols.rbak import Target, Source
from zensols.rbak import Executor

logger = logging.getLogger('zensols.rbak.backup')

class Backuper(object):
    """
    This class runs backups from sources to targets.
    """
    def __init__(self, config, source_names=None, dry_run=True, executor=None):
        self.config = config
        self.source_names = source_names
        self.executor = executor if executor else Executor(logger, dry_run)
        self.backup_cmd = config.get_option('backup_cmd', expect=True)

    @property
    def dry_run(self):
        return self.executor.dry_run

    @property
    def targets(self):
        "Get all configured targets."
        if not hasattr(self, '_targets'):
            target_names = self.config.get_option_list('targets', expect=True)
            self._targets = [Target(l, self.executor, self.config) for l in target_names]
        return self._targets

    @property
    def sources(self):
        "Get all configured sources."
        if not hasattr(self, '_sources'):
            if self.source_names is not None:
                source_names = self.source_names.split(' ')
            else:
                source_names = self.config.get_option_list('sources', expect=True)
            self._sources = [Source(l, self.config) for l in source_names]
        return self._sources

    def info(self):
        "Print source and target configuration."
        print('sources:')
        for targ in self.sources:
            print('  {}'.format(targ))
        print('targets:')
        for targ in self.targets:
            print('  {}'.format(targ))

    def mount_all(self):
        "Mount all mountable targets."
        for targ in self.targets:
            logger.info('mounting: {}'.format(targ))
            try:
                targ.mount()
            except OSError as e:
                logger.error('''can't mount {}--skipping'''.format(targ))
                continue

    def umount_all(self):
        "Umount all mountable targets."
        for targ in self.targets:
            logger.info('un-mounting: {}'.format(targ))
            try:
                targ.umount()
            except OSError as e:
                logger.error('''can't un-mount {}--skipping'''.format(targ))
                continue

    def sync(self):
        """
        Use rsync to backup files.
        """
        mounts = []
        for targ in self.targets:
            if targ.mountable and not targ.is_mounted:
                try:
                    targ.mount()
                    mounts.append(targ)
                except OSError as e:
                    logger.error('''can't mount {}--skipping'''.format(targ))
                    continue
            if not os.path.isdir(targ.backup_path):
                logger.info('creating path: {}'.format(targ.backup_path))
                if not self.dry_run:
                    pathlib.Path(targ.backup_path).mkdir(parents=True, exist_ok=True)
            for source in self.sources:
                cmd_ctx = {'source': source, 'target': targ}
                logger.info('{} -> {}'.format(source.path, targ.backup_path))
                cmd = self.backup_cmd.format(**cmd_ctx)
                self.executor.run(cmd)
        for mnt in mounts:
            mnt.umount()
