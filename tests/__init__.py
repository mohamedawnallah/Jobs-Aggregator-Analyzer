
import sys
import os

parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
path = os.path.join(parent_path, 'app')
os.chdir(path)
sys.path.append(path)