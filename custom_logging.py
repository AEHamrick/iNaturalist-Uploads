import os, sys, pendulum, logging
import pendulum
from pathlib import Path

def create_logger(logpath:Path, basename) -> logging.Logger:

    fmt = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S ')
    
    hnd = logging.FileHandler(logpath / '{0}.log'.format(basename))
    
    hnd.setFormatter(fmt)
    
    logger = logging.Logger('iNat')
    
    logger.addHandler(hnd)
    
    return logger