
class InvalidConfigurationException(BaseException):
    '''Exception indicating that some config is not setup correctly'''
    def __init__(self, expFile, msg=''):
        super(InvalidConfigurationException, self).__init__()
        self.expFile = expFile
        self.msg = msg
        self.configSpec = 'Config'

    def __str__(self):
        return (self.configSpec + ' file: ' + self.expFile + ' is incorrect. ' +
            'Please read documentation. ' +
            (('Exact error cause:' + self.msg) if len(self.msg) > 0 else ''))
