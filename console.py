import sys
import re

from all_estimator import *

def help():
    print(
        "============================================input error ================================================")
    print("input format of exact LPN: console.py N=1024 k=652 t=57 exact")
    print("============================================================================================")
    print("or console.py N=1024 k=652 t=57 q=13 exact #(bit security of exact LPN with field size q")
    print("or console.py n=1024 N=4096 t=88 exact #(bit security of dual exact LPN)")

    print("or console.py n=1024 N=4096 t=88 q=13 exact #(bit security of dual exact LPN with field size q")
    print("============================================================================================")
    print("input format of regular LPN: console.py N=1024 k=652 t=57 regular")

    print("or console.py N=1024 k=652 t=57 q=13 regular #(bit security of regular LPN with field size q")
    print("or console.py n=1024 N=4096 t=88 regular #(bit security of dual regular LPN)")

    print("or console.py n=1024 N=4096 t=88 q=13 regular #(bit security of dual regular LPN with field size q")
    print(f"============================================================================================")
    print(f"input format of rank syndrome decoding: console.py n=82 k=41 t=4 q=2 m=41")
    print("============================================================================================")
    print(f"input format of SIS: console.py n=2048 q=83804 bound=3502")
    print()

#####################      main() function   ###########################

def main():
    # print(len(sys.argv))
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        help()
    elif 'n' in sys.argv[1] and 'N' in sys.argv[2] and 't' in sys.argv[3]:
        n = int(re.findall(r"\d+", sys.argv[1]).pop())
        N = int(re.findall(r"\d+", sys.argv[2]).pop())
        t = int(re.findall(r"\d+", sys.argv[3]).pop())

        if len(sys.argv) == 5 and 'x' in sys.argv[-1]:
            print("bit security of dual exact LPN (n=" + str(n) + ", N=" + str(N) + ", t=" + str(t) + "):",end='')
            res = analysisfordual2(n, N, t)
            res = round(res)
            print(res)
            print(f"quantum security is:{res // 2}")
            # print(analysisfordual2(n, N, t))
            # print()

        elif len(sys.argv) == 5 and 'r' in sys.argv[-1]:
            print("bit security of dual regular LPN (n=" + str(n) + ", N=" + str(N) + ", t=" + str(t) + "):",end='')
            res = analysisfordual2regular(n, N, t)
            res = round(res)
            print(res)
            print(f"quantum security is:{res // 2}")
            # print(analysisfordual2regular(n, N, t))
            # print()

        elif 'q' in sys.argv[-2] and 'x' in sys.argv[-1]:
            q = int(re.findall(r"\d+", sys.argv[-2]).pop())
            print("bit security of dual exact LPN (n=" + str(n) + ", N=" + str(N) + ", t=" + str(t) + ", q=" + str(
                q) + "):",end='')
            res = analysisfordualq(n, N, t, q)
            res = round(res)
            print(res)
            print(f"quantum security is:{res // 2}")
            # print(analysisfordualq(n, N, t, q))
            # print()

        elif 'q' in sys.argv[-2] and 'r' in sys.argv[-1]:
            q = int(re.findall(r"\d+", sys.argv[-2]).pop())
            print(
                "bit security of regular LPN (n=" + str(n) + ", N=" + str(N) + ", t=" + str(t) + ", q=" + str(q) + "):",end='')
            res = analysisfordualqregular(n, N, t, q)
            res = round(res)
            print(res)
            print(f"quantum security is:{res // 2}")
            # print(analysisfordualqregular(n, N, t, q))
            # print()

        else:
            help()


    elif 'N' in sys.argv[1] and 'k' in sys.argv[2] and 't' in sys.argv[3]:
        N = int(re.findall(r"\d+", sys.argv[1]).pop())
        k = int(re.findall(r"\d+", sys.argv[2]).pop())
        t = int(re.findall(r"\d+", sys.argv[3]).pop())

        if len(sys.argv) == 5 and 'x' in sys.argv[-1]:
            print("bit security of exact LPN (N=" + str(N) + ", k=" + str(k) + ", t=" + str(t) + "):",end='')
            res = analysisfor2(N, k, t)
            res = round(res)
            print(res)
            print(f"quantum security is:{res // 2}")
            # print(analysisfor2(N, k, t))
            # print()

        elif len(sys.argv) == 5 and 'r' in sys.argv[-1]:
            print("bit security of regular LPN (N=" + str(N) + ", k=" + str(k) + ", t=" + str(t) + "):",end='')
            res = analysisfor2regular(N, k, t)
            res = round(res)
            print(res)
            print(f"quantum security is:{res // 2}")
            # print(analysisfor2regular(N, k, t))
            # print()

        elif 'q' in sys.argv[-2] and 'x' in sys.argv[-1]:
            q = int(re.findall(r"\d+", sys.argv[-2]).pop())
            print("bit security of exact LPN (N=" + str(N) + ", k=" + str(k) + ", t=" + str(t) + ", q=" + str(
                q) + "):",end='')
            res = analysisforq(N, k, t, q)
            res = round(res)
            print(res)
            print(f"quantum security is:{res//2}")


        elif 'q' in sys.argv[-2] and 'r' in sys.argv[-1]:
            q = int(re.findall(r"\d+", sys.argv[-2]).pop())
            print("bit security of regular LPN (N=" + str(N) + ", k=" + str(k) + ", t=" + str(t) + ", q=" + str(
                q) + "):",end='')
            res = analysisforqregular(N, k, t, q)
            res = round(res)
            print(res)
            print(f"quantum security is:{res//2}")
            print()

        else:
            help()

    elif 'n' in sys.argv[1] and 'k' in sys.argv[2] and 't' in sys.argv[3] and 'q' in sys.argv[4] and 'm' in sys.argv[5]:
        n = int(re.findall(r"\d+", sys.argv[1]).pop())
        k = int(re.findall(r"\d+", sys.argv[2]).pop())
        t = int(re.findall(r"\d+", sys.argv[3]).pop())
        q = int(re.findall(r"\d+", sys.argv[4]).pop())
        m = int(re.findall(r"\d+", sys.argv[5]).pop())
        res = analysisforrank(n,k,t,q,m)
        res = round(res)
        print("bit security of rank SD (n=" + str(n) + ", k=" + str(k) + ", t=" + str(t) + ", q=" + str(q) + ", m=" + str(m) +  "):",end='')
        print(res)
        print(f"quantum security is:{res//2}")
        print()

    elif 'n' in sys.argv[1] and 'q' in sys.argv[2] and 'b' in sys.argv[3]:
        n = int(re.findall(r"\d+", sys.argv[1]).pop())
        q = int(re.findall(r"\d+", sys.argv[2]).pop())
        b = int(re.findall(r"\d+", sys.argv[3]).pop())
        res = analysisforsis(n,q,b)
        classic = round(res["classical_equiv"])
        quant = round(res['quantum_equiv'])
        print(f"bit security of SIS:{classic}")
        # print(classic)
        print(f"quantum security is:{quant}")
        print()



    else:
        help()

if __name__ == '__main__':
    main()