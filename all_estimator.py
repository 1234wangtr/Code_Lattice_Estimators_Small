from lwyy.hardness_of_lpn import *
from rank.rank_sd_estimator import *
from sis.sis_estimator import *


#####################      Bit security of LPN and dual LPN     ###########################
# We propose a non-asymptotic cost of the information set decoding algorithm, Pooled Gauss attack, and statistical decoding attack
# against the LPN problem over finite fields F_q or a ring Z_{2^\lambda} with parameters

# LPN parameters: N (number of queries),
#                k (length of secret),
#                t (Hamming weight of noise),
#                q (size of field) and
#                lambda (bit size of ring)

# dual LPN parametersï¼šn (corresponding to the number of COT/VOLE correlations),
#                     N (number of queries),
#                     t (Hamming weight of noise),
#                     q (size of field) and
#                     lambda (bit size of ring)

# noise parameters: exact or regular. Noise parameters can be either exact or regular. Default functions apply to exact noise, unless labeled as "regular".


def analysisfor2(N, k, t):
    # LWYY
    T1 = Gauss(N, k, t)
    print(f"Gauss={T1}")
    T2 = SD_ISD(N, k, t)
    print(f"SDISD={T2}")
    T3 = BJMM_ISD(N, k, t)
    print(f"BJMM={T3}")


    return min(T1, T2, T3)


def analysisfor2regular(N, k, t):
    # LWYY
    N1 = N - t
    k1 = k - t
    T1 = analysisfor2(N1, k1, t)


    # dbg
    print(f"ISD={T1}")

    return T1


def analysisfordual2(n, N, t):
    k = N - n
    return analysisfor2(N, k, t)


def analysisfordual2regular(n, N, t):
    k = N - n

    return analysisfor2regular(N, k, t)


def analysisforq(N, k, t, q):
    if q==2:
        return analysisfor2(N,k,t)
    # LWYY
    T1 = SD_ISD_q(N, k, t, q)
    # T2 = SDforq(N, k, t)
    T3 = Gauss(N, k, t)
    # T4 = SD2forq(N, k, t, q)

    return min(T1, T3)


def analysisforqregular(N, k, t, q):
    if q==2:
        return analysisfor2regular(N,k,t)
    # LWYY
    T1 = analysisforq(N, k, t, q)


    # dbg
    # print(f"ISD={T1}")

    return T1


def analysisfordualq(n, N, t, q):
    k = N - n

    return analysisforq(N, k, t, q)


def analysisfordualqregular(n, N, t, q):
    k = N - n
    return analysisforqregular(N, k, t, q)


def analysisforrank(n,k,r,q,m):
    T1 = optimized_GRS(n,k,r,q,m)
    return T1

def analysisforsis(n,q,b):
    T = estimate_sis(n,q,b)
    return T