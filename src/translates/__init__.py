# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
import os

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'


ROOT_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(ROOT_PATH, '..', '..', 'data')
