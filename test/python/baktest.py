#!/usr/bin/env python

import logging
import unittest
import sys
from zensols.rbak import Backuper, Executor
from zensols.actioncli import Config

#logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('zensols.rbak.test')

class PushExecutor(Executor):
    def __init__(self):
        super(PushExecutor, self).__init__(logger, True)
        self.cmds = []

    def run(self, cmd):
        self.cmds.append(cmd)

class TestBackuper(unittest.TestCase):
    def test_read_targs(self):
        conf = Config('test-resources/rbak.conf')
        bak = Backuper(conf, dry_run=True)
        targs = bak.targets
        self.assertEqual(2, len(targs))
        targ = targs[0]
        self.assertEqual('extbak2t', targ.name)
        self.assertEqual('/mnt/extbak2t', targ.path)
        self.assertEqual('bak', targ.backup_dir)
        self.assertEqual('/mnt/extbak2t/bak', targ.backup_path)

    def test_read_targs_path(self):
        conf = Config('test-resources/rbak.conf')
        bak = Backuper(conf, dry_run=True)
        targ = bak.targets[1]
        self.assertEqual('hdbak1', targ.name)
        self.assertEqual('/opt/hd1', targ.path)
        self.assertEqual('', targ.backup_dir)
        self.assertEqual('/opt/hd1', targ.backup_path)

    def test_try_mount(self):
        conf = Config('test-resources/rbak.conf')
        bak = Backuper(conf, dry_run=False)
        targ = bak.targets[1]
        def mfn():
            targ.mount()
        self.assertRaises(ValueError, mfn)

    def test_read_sources(self):
        conf = Config('test-resources/rbak.conf')
        bak = Backuper(conf, dry_run=True)
        sources = bak.sources
        self.assertEqual(2, len(sources))
        self.assertEqual('/opt/var/git', sources[0].path)
        self.assertEqual('git', sources[0].basename)
        self.assertEqual('/opt/var/svn', sources[1].path)
        self.assertEqual('other/svndir', sources[1].basename)

    def test_mount(self):
        conf = Config('test-resources/rbak.conf')
        ex = PushExecutor()
        bak = Backuper(conf, executor=ex, dry_run=True)
        targ = bak.targets[0]
        targ.mount()
        self.assertEqual(['/bin/mount -L extbak2t /mnt/extbak2t'], ex.cmds)

    def test_sync(self):
        conf = Config('test-resources/rbak.conf')
        ex = PushExecutor()
        bak = Backuper(conf, executor=ex, dry_run=True)
        bak.sync()
        cmds = ['/bin/mount -L extbak2t /mnt/extbak2t',
                'rsync -rltpgoDuv -n /opt/var/git/ /mnt/extbak2t/bak/git',
                'rsync -rltpgoDuv -n /opt/var/svn/ /mnt/extbak2t/bak/other/svndir',
                'rsync -rltpgoDuv -n /opt/var/git/ /opt/hd1/git',
                'rsync -rltpgoDuv -n /opt/var/svn/ /opt/hd1/other/svndir']
        self.assertEqual(cmds, ex.cmds)
