import os, sys, pendulum, logging
import pendulum
from pathlib import Path

def create_logger(logpath:Path, basename) -> logging.Logger:

    fmt = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S ')
    
    #Doesn't seem like any need for a rotating file handler or anything fancy given the volume of usage
    hnd = logging.FileHandler(logpath / '{0}.log'.format(basename))
    
    s_hnd = logging.StreamHandler(stream=sys.stdout)
    
    hnd.setFormatter(fmt)
    s_hnd.setFormatter(fmt)
    logger = logging.getLogger()
    
    logger.setLevel(logging.DEBUG)
    logger.addHandler(hnd)
    logger.addHandler(s_hnd)
    
    logger.info('Logging set up')
    
    return logger