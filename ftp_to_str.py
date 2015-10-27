import ftplib
import logging
import StringIO

version = 1.0
logger = logging.getLogger('ftp_to_str')


# Exceptions
class FTPError(Exception):
    '''All exceptions in ftp_to_str inherits from this exception'''

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class TransferError(FTPError):
    '''Exceptions related to FTP connection and file transfer issues'''

class ReadError(FTPError):
    '''Exceptions related file reading and string convertion issues'''


def ftp_to_str(host=None, file_path=None, **kwargs): 
    '''Retrives a file with FTP and returns a string with the content.
    Raises TransferError or ReadError exceptions in case of issues'''

    port = kwargs.get('port', 21)
    user = kwargs.get('user', None)
    password = kwargs.get('password', None)
    timeout = kwargs.get('timeout', 30)
    passive_mode = kwargs.get('passive_mode', True)
    
    # Checks if mandatory arguments are provided
    if not host or not file_path:
        raise TypeError('"host" and "file_path" argument is required')

    if (user and not password) or (password and not user):
        raise TypeError(
            '"user" and "password" argument is required for authentication')

    if not isinstance(port, int):
        raise TypeError('Argument "port" must be a integer')

    logger.info('Trying to open FTP connection to %s:%i' % (host, port))

    try:
        session = ftplib.FTP()
        session.connect(host, port, timeout)

        if user and password:
            logger.debug('Attempting login in with user "%s"' % user)

        else:
            logger.debug('Attempting to login anonymously')

        session.login(user, password)

        if not passive_mode:
            logger.debug('Disabling passive transfer mode')

        session.set_pasv(passive_mode)
        
        logger.info('Trying to retrive file "%s"' % file_path)
        download_target = StringIO.StringIO()
        session.retrlines('RETR ' + file_path, download_target.write)

        logger.debug('Reading file data')
        content_string = str(download_target.getvalue())

        logger.debug('Closing StringIO object and FTP connection')
        download_target.close()
        session.quit()

        return content_string

    except ftplib.all_errors as error:
        raise TransferError('Failed to retrive file from FTP: "%s"' % error)

    except (ValueError, TypeError):
        raise ReadError('Failed to read or transform file "%s"' % file_path)

    except Exception as exception:
        raise FTPError(
            'Failed to retrive or read file due to unknown issue: "%s"'
            % str(exception))

    finally:
        try:
            # Make sure to tear down the FTP session in case of error
            download_target.close()
            session.quit()

        except:
            # This could cause an issue if the session does not exist
            pass
