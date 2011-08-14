import os.path
import util
import model
from model import *

def file(*subpaths):
	return os.path.join(__path__[0], *subpaths)
