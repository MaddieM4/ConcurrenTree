import os.path
import util
import model
from model import *

__all__ = ["model", "util"]

def file(*subpaths):
	return os.path.join(__path__[0], *subpaths)
