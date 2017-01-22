# -*- coding: utf-8 -*-

from __future__ import print_function

import atexit
import functools
import hashlib
import os
import pickle
import shutil


CACHE_FOLDER = os.path.join('cache')


class Cached(object):
    def __init__(self, func):
        self.func = func
        self.cache = None
        atexit.register(self.save)
        self.modified = False

    def __call__(self, *args, **kwargs):
        fkey = args[0].__class__.__name__ + '_' + self.func.__name__
        self.filepath = os.path.join(CACHE_FOLDER, fkey + '.obj')

        if self.cache is None:
            if os.path.exists(self.filepath):
                print('loading', self.filepath, '...')
                with open(self.filepath, 'rb') as infile:
                    self.cache = pickle.load(infile)
            else:
                self.cache = {}

        pickled = pickle.dumps(args[1:], -1) + pickle.dumps(kwargs, -1)
        key = hashlib.sha1(pickled).hexdigest()
        try:
            return self.cache[key]
        except KeyError:
            # print(fkey, 'key not found...')
            self.modified = True
            value = self.func(*args, **kwargs)
            self.cache[key] = value
            return value

    def __get__(self, inst, objtype):
        return functools.partial(self.__call__, inst)

    def save(self):
        if not self.cache:
            return
        if not self.modified:
            # no need to save unmodified cache
            return
        if not os.path.exists(CACHE_FOLDER):
            os.makedirs(CACHE_FOLDER)
        with open(self.filepath, 'wb') as outfile:
            pickle.dump(self.cache, outfile, -1)

    @staticmethod
    def clear_cache():
        shutil.rmtree(CACHE_FOLDER)


