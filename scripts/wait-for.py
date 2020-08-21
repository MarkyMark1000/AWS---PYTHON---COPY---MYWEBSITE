'''
I don't like adding this in here, but I cannot get the typical wait-for scripts
to work with MySQL database in docker, so I have written a python script that
either times out after ? seconds or successfully connects to the database
The input arguments for the script need to be:

    HOST, PORT, USERNAME, PASSWORD, DATABASE, TIMEOUT

I tried includting the wait-for script recommended on the docker website:
   https://docs.docker.com/compose/startup-order/

However I kept getting an 'Operation timed out' error from the logs, hence the
use of this script.

'''

import sys
import os
import time
import pymysql


def readCommandLineArgument():

    # Validate the number of command line input arguments and return the
    # input filename

    # Get arguments
    if len(sys.argv) != 7:
        raise ValueError("You must pass in 6 arguments, HOST, PORT, "
                         "USERNAME, PASSWORD, DATABASE, TIMEOUT")

    # return the arguments as a tuple
    return (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
            sys.argv[6])


def connectToDB(HOST, PORT, USERNAME, PASSWORD, DATABASE):

    # for now, just try to connect to the database.

    con = pymysql.connect(host=HOST, port=PORT, user=USERNAME,
                          password=PASSWORD, database=DATABASE)

    with con.cursor() as cur:
        cur.execute("SELECT VERSION()")


def runDelay():

    # I dont like passing passwords in, but this is only used for a test
    # docker delay script

    # Get the database connection characteristics.
    (HOST, PORT, USERNAME, PASSWORD, DATABASE, TIMEOUT) = \
                readCommandLineArgument()

    # Ensure timeout is an integer greater than zero, otherwise use 15 secs
    # a default
    try:
        TIMEOUT = int(TIMEOUT)
        if TIMEOUT <= 0:
            raise("Timeout needs to be > 0")
    except Exception as Ex:
        TIMEOUT = 60

    # Ensure port is an integer greater than zero, otherwise use 3306 as
    # default
    try:
        PORT = int(PORT)
        if PORT <= 0:
            raise("Port needs to be > 0")
    except Exception as Ex:
        PORT = 3306

    # Try to connect to the database TIMEOUT times
    for i in range(0, TIMEOUT):

        try:
            # Try to connect to db
            connectToDB(HOST, PORT, USERNAME, PASSWORD, DATABASE)

            # If an error hasn't been raised, then exit
            return True

        except Exception as Ex:
            print(Ex.args)
            # Sleep for 1 second
            time.sleep(1)

    # If I get here, assume a timeout has occurred
    raise("Timeout")


if __name__ == "__main__":

    runDelay()
