#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: interface.py
# Date: Fri Dec 27 02:59:09 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from collections import defaultdict
#from sklearn.mixture import GMM
from scipy.io import wavfile
import time
import cPickle as pickle
from filters.VAD import VAD

from feature import mix_feature

from gmmset import GMMSetPyGMM as GMMSet

class ModelInterface(object):

    def __init__(self):
        self.features = defaultdict(list)
        self.gmmset = GMMSet()
        self.vad = VAD()

    def init_noise(self, fs, signal):
        self.vad.init_noise(fs, signal)

    def filter(self, fs, signal):
        return self.vad.filter(fs, signal)

    def enroll(self, name, fs, signal):
        feat = mix_feature((fs, signal))
        self.features[name].extend(feat)

    def train(self):
        self.gmmset = GMMSet()
        start = time.time()
        print "Start training..."
        for name, feats in self.features.iteritems():
            self.gmmset.fit_new(feats, name)
        print time.time() - start, " seconds"

    def predict(self, fs, signal):
        feat = mix_feature((fs, signal))
        return self.gmmset.predict(feat)

    def dump(self, fname):
        with open(fname, 'w') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(fname):
        with open(fname, 'r') as f:
            return pickle.load(f)


if __name__ == "__main__":
    m = ModelInterface()
    fs, signal = wavfile.read("../corpus.silence-removed/Style_Reading/f_001_03.wav")
    m.enroll('h', fs, signal[:80000])
    fs, signal = wavfile.read("../corpus.silence-removed/Style_Reading/f_003_03.wav")
    m.enroll('a', fs, signal[:80000])
    m.train()
    print m.predict(fs, signal[:80000])
