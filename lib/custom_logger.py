import logging
import os
from pathlib import Path
import sys

"""
DEBUG
Detailed information, typically of interest only when diagnosing problems.
INFO
Confirmation that things are working as expected.
WARNING
An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
ERROR
Due to a more serious problem, the software has not been able to perform some function.
CRITICAL
A serious error, indicating that the program itself may be unable to continue running.
"""

logging.basicConfig( 
    # format="[%(asctime)s]  %(levelname)-5s: %(filename)s:%(lineno)-5d: %(message)s",
    # format="%(levelname)-5s: %(filename)s:%(lineno)-5d: %(message)s",
    format='{"level": "%(levelname)s", "filename": "%(filename)s", "line_no": %(lineno)s',
    datefmt="%Y-%m-%d %H:%M:%S", 
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("plant-pot-backend")