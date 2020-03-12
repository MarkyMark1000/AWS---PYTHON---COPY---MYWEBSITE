import boto3

import logging
logger = logging.getLogger('ebdjango')


class AWSParameterStore():
    '''
    This class is to help extract information from AWS Parameter Store, such as database user id's, passwords
    etc etc
    '''

    def __init__(self, strProject, strEnvironment, strRegion):
        '''
        Assume my keys are stored in the format:
           /strProject/strEnvironment/strKey
        '''
        logger.debug('Logging debug message')

        self._client = boto3.client('ssm', region_name=strRegion)
        self._project = '/'+(strProject.rstrip('/')+'/').lstrip('/')
        self._environment = strEnvironment.strip('/')

    def get_parameter(self, strKey, boolDecrypt):
        '''
        Build key in form /strProject/strEnvironment/strKey, then extract it
         from client
        '''

        logger.debug('Logging debug message')

        strIn = self._project + self._environment + '/' + strKey

        param = self._client.get_parameter(Name=strIn,
                                           WithDecryption=boolDecrypt)

        strRet = param['Parameter']['Value']

        if len(strRet.strip()) < 1:
            logger.error('AWSParamStore error for {key}'.format(key=strKey))
            raise Exception("zero length parameter from parameter store !!!")

        return strRet
