class RigaPresenteException(Exception):
    '''
    Lanciata quando si tenta di inserire nel database una tupla gia' presente
    '''

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
