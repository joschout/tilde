import numpy as np
import scipy as sp
import scipy.stats


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t.ppf((1+confidence)/2., n-1)
    return m, m-h, m+h, h


def run_financial_data():
    data = [0.86956521739130432, 0.86956521739130432, 0.82608695652173914, 0.86956521739130432, 0.86956521739130432,
            0.875, 0.82608695652173914, 0.875, 0.83333333333333337, 0.875]

    confidence = 0.9
    m, m_minus_h, m_plus_h, h = mean_confidence_interval(data, confidence=confidence)

    print("confidence: ", confidence)
    print("mean: ", m)
    print("diff: ", h)
    print("lower: ", m_minus_h)
    print("upper: ", m_plus_h)


def run_mutaace1_data():
    data = [0.60869565217391308, 0.625, 0.66666666666666663, 0.70833333333333337, 0.69999999999999996, 0.54166666666666663, 0.625, 0.69999999999999996, 0.70833333333333337, 0.65217391304347827]
    confidence = 0.9

    m, m_minus_h, m_plus_h, h = mean_confidence_interval(data, confidence=confidence)

    print("confidence: ", confidence)
    print("mean: ", m)
    print("diff: ", h)
    print("lower: ", m_minus_h)
    print("upper: ", m_plus_h)

if __name__ == '__main__':
    print("financial:")
    run_financial_data()
    print("mutaace1;")
    run_mutaace1_data()


