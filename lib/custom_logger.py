import logging
import os
from pathlib import Path

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
    format="[%(asctime)s] %(filename)s:%(lineno)-5d %(levelname)-8s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S", 
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("plant-pot-backend")