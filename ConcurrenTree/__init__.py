import os.path
import model
from model import *

__all__ = ["model", "storage"]

def file(*subpaths):
	return os.path.join(__path__[0], *subpaths)
