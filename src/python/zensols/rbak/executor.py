import os

class Executor(object):
    def __init__(self, logger, dry_run=False, check_exit_value=0):
        self.logger = logger
        self.dry_run = dry_run
        self.check_exit_value = check_exit_value

    def run(self, cmd):
        self.logger.info('system <{}>'.format(cmd))
        if not self.dry_run:
            ret = os.system(cmd)
            self.logger.debug('exit value: {} =? {}'.format(ret, self.check_exit_value))
            if self.check_exit_value is not None and ret != self.check_exit_value:
                msg = 'command returned with {}, expecting {}'.\
                      format(ret, self.check_exit_value)
                raise OSError(msg)
