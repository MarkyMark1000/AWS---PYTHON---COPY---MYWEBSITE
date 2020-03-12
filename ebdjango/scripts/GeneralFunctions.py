import requests

import logging
logger = logging.getLogger('ebdjango')

def appendEC2IPToArray(inputArray):
    '''
    Once I started filling ALLOWED_HOSTS with specific addresses, the health of the
    Elastic Beanstalk Environments started degrading.   By getting the EC2 IP address and
    adding it to ALLOWED_HOSTS, this prevents health degredation.
    '''

    logger.debug('Logging debug message')

    try:
        # Try to get the IP
        EC2_PRIVATE_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4',
                                  timeout=0.01).text
        # If we get an IP, append it to the array
        if EC2_PRIVATE_IP:
            if EC2_PRIVATE_IP not in inputArray:
                inputArray.append(EC2_PRIVATE_IP)
            return True
        else:
            return False
    except Exception as Ex:
        # Do nothing if there is an error
        logger.error('appendEC2IPToArray')
        return False