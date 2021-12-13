#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import *
from controller import *
from sql import create_tables
import time
if __name__ == '__main__':
    time.sleep(3)
    create_tables()
    server.run()