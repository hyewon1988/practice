#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x:
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    words = x.split()
    return {word:words.count(word) for word in words}

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    weights = {}  # feature => weight
    for train_example in trainExamples:
        phi = featureExtractor(train_example[0])
        y = train_example[1]
        # hinge loss
        loss = 1 - dotProduct(phi, weights) * y
        # update weights
        if loss > 0 :
            increment(weights, y*eta, phi)
    return weights

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        features = random.sample(weights.keys(), random.randint(1, len(weights.keys())))
        phi = {feature: random.randint(1, 10) for feature in features}
        y = 1 if dotProduct(phi,weights) > 0 else -1
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3e: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        x = x.replace(' ', '')
        words = [x[i:i+n] for i in range(len(x)-n+1)]
        return {word: words.count(word) for word in words}
    return extract

############################################################
# Problem 4: k-means
############################################################


def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    def get_dist(x1, x2):
        keys = set(x1.keys() + x2.keys())
        return sum([(x2[key] - x1[key])**2 for key in keys])

    centers = random.sample(examples, K)
    assignments = [0] * len(examples)
    old_cost = 0

    for iter in range(maxIters):
        # assignments
        for i in range(len(examples)):
            new_cost = 0
            dist = [get_dist(center, examples[i]) for center in centers]
            min_dist = min(dist)
            min_center_idx = dist.index(min_dist)
            assignments[i] = min_center_idx
            new_cost += min_dist

        if new_cost == old_cost:
            break
        else:
            old_cost = new_cost

        # update
        centers = [{} for i in range(K)]
        nums = [0 for i in range(K)]

        for i in range(len(examples)):
            nums[assignments[i]] += 1
            increment(centers[assignments[i]], 1, examples[i])

        for k in range(K):
            for key in examples[i].keys():
                centers[k][key] /= nums[k]

    return centers, assignments, old_cost
