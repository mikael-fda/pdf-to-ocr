#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from redis import Redis
from rq import Queue

from my_count import count_n_w

from server import *
from controller import *

redis = Redis(host="redis")
queue = Queue(name="ocr", connection=redis)


names = "Marc Jack Alfred".split()
words = "je suis une fussé et pas un mot".split()

def count_size_of():
    random.shuffle(names)
    random.shuffle(words)
    
    name = names[0]
    word = words[0]
    
    queue.enqueue(count_n_w, args=(name, word))

if __name__ == '__main__':
    server.run()
    
#if __name__ == "__main__":
#    count_size_of()