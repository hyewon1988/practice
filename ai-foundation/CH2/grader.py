#!/usr/bin/python

import util
import time
import unittest
from util import *
from submission import *

class CH2TestCase(unittest.TestCase):
    ############################################################
    # Problem 3: sentiment classification
    ############################################################

    ### 3a

    # Basic sanity check for feature extraction
    def test3a0(self):
        ans = {"a":2, "b":1}
        submission = extractWordFeatures("a b a")
        self.assertEqual(ans, submission)

    def test3a1(self):
        random.seed(42)
        for i in range(10):
            sentence = ' '.join([random.choice(['a', 'aa', 'ab', 'b', 'c']) for _ in range(100)])
        submission_ans = extractWordFeatures(sentence)
        print submission_ans


    ### 3b
    def test3b0(self):
        trainExamples = (("hello world", 1), ("goodnight moon", -1))
        testExamples = (("hello", 1), ("moon", -1))
        featureExtractor = extractWordFeatures
        weights = learnPredictor(trainExamples, testExamples, featureExtractor, numIters=20, eta=0.01)
        self.assertGreater(weights["hello"], 0)
        self.assertLess(weights["moon"], 0)


    def test3b1(self):
        trainExamples = (("hi bye", 1), ("hi hi", -1))
        testExamples = (("hi", -1), ("bye", 1))
        featureExtractor = extractWordFeatures
        weights = learnPredictor(trainExamples, testExamples, featureExtractor, numIters=20, eta=0.01)
        self.assertLess(weights["hi"], 0)
        self.assertGreater(weights["bye"], 0)

    ### 3c
    def test3c0(self):
        weights = {"hello":1, "world":1}
        data = generateDataset(5, weights)
        for datapt in data:
            self.assertGreaterEqual(dotProduct(datapt[0], weights), 0)
            self.assertEqual(datapt[1], 1)

    def test3c1(self):
        weights = {}
        for i in range(100):
            weights[str(i + 0.1)] = 1
        data = generateDataset(100, weights)
        for datapt in data:
            self.assertNotEqual(dotProduct(datapt[0], weights), 0)
    ### 3e

    def test3e0(self):
        fe = extractCharacterFeatures(3)
        sentence = "hello world"
        ans = {"hel":1, "ell":1, "llo":1, "low":1, "owo":1, "wor":1, "orl":1, "rld":1}
        self.assertEqual(fe(sentence), ans)

    def test3e1(self):
        random.seed(42)
        for i in range(10):
            sentence = ' '.join([random.choice(['a', 'aa', 'ab', 'b', 'c']) for _ in range(100)])
            for n in range(1, 4):
                submission_ans = extractCharacterFeatures(n)(sentence)
                #print submission_ans

    ############################################################
    # Problem 4: clustering
    ############################################################

    # basic test for k-means
    def test4b0(self):
        x1 = {0:0, 1:0}
        x2 = {0:0, 1:1}
        x3 = {0:0, 1:2}
        x4 = {0:0, 1:3}
        x5 = {0:0, 1:4}
        x6 = {0:0, 1:5}
        examples = [x1, x2, x3, x4, x5, x6]
        centers, assignments, totalCost = kmeans(examples, 2, maxIters=10)
        # (there are two stable centroid locations)
        self.assertTrue(round(totalCost, 3)==4 or round(totalCost, 3)==5.5 or round(totalCost, 3)==5.0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
