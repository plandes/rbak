from zensols.actioncli import OneConfPerActionOptionsCliEnv
from zensols.actioncli import ExtendedInterpolationEnvConfig as AppConfig
from zensols.rbak import Backuper


# recommended app command line
class ConfAppCommandLine(OneConfPerActionOptionsCliEnv):
    def __init__(self):
        dry_run_op = ['-d', '--dryrun', False,
                      {'dest': 'dry_run',
                       'action': 'store_true', 'default': False,
                       'help': 'dry run to not actually connect, but act like it'}]
        sources_op = ['-n', '--sources', False,
                      {'dest': 'source_names',
                       'help': 'override the sources property in the config'}]
        cnf = {'executors':
               [{'name': 'backup',
                 'executor': lambda params: Backuper(**params),
                 'actions': [{'name': 'info',
                              'doc': 'print backup configuration information'},
                             {'name': 'backup',
                              'meth': 'sync',
                              'doc': 'run the backup',
                              'opts': [dry_run_op, sources_op]},
                             {'name': 'mount',
                              'meth': 'mount_all',
                              'doc': 'mount all targets',
                              'opts': [dry_run_op]},
                             {'name': 'umount',
                              'meth': 'umount_all',
                              'doc': 'un-mount all targets',
                              'opts': [dry_run_op]}]}],
               # uncomment to add a configparse (ini format) configuration file
               'config_option': {'name': 'config',
                                 'opt': ['-c', '--config', False,
                                         {'dest': 'config', 'metavar': 'FILE',
                                          'default': '/etc/rbak.conf',
                                          'help': 'configuration file'}]},
               'whine': 1}
        super().__init__(cnf, config_env_name='rbakrc',
                         pkg_dist='zensols.rbak',
                         config_type=AppConfig, no_os_environ=True)


def main():
    cl = ConfAppCommandLine()
    cl.invoke()
