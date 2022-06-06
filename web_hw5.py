import time
import multiprocessing as Mlp


def factorize(cnt: int):
    result = []
    for _ in range(cnt):
        if cnt % (_+1) == 0:   # avoid div by 0  (_+1) and full range
            result.append(_+1)
    print(result)
    return result


if __name__ == "__main__":
    # for single serial process
    print("for serial single process")
    start_time = time.time()
    fact128 = factorize(128)
    fact255 = factorize(255)
    fact99999 = factorize(99999)
    fact10651060 = factorize(10651060)
    end_time = time.time()
    print("exec_time = ", (end_time - start_time), 's')
    # testing result
    assert fact128 == [1, 2, 4, 8, 16, 32, 64, 128]
    assert fact255 == [1, 3, 5, 15, 17, 51, 85, 255]
    assert fact99999 == [1, 3, 9, 41, 123, 271, 369, 813, 2439,
                         11111, 33333, 99999]
    assert fact10651060 == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70,
                            140, 76079, 152158, 304316, 380395, 532553,
                            760790, 1065106, 1521580, 2130212, 2662765,
                            5325530, 10651060]

    # for multiprocess as Process
    Mlp.set_start_method('spawn')  # Windows OS
    p1 = Mlp.Process(target=factorize, args=(128,))
    p2 = Mlp.Process(target=factorize, args=(255,))
    p3 = Mlp.Process(target=factorize, args=(99999,))
    p4 = Mlp.Process(target=factorize, args=(10651060,))
    print("for multiprocess as Process")
    start_time = time.time()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()    # print visible only in cmd.exe
    p2.join()
    p3.join()
    p4.join()
    end_time = time.time()
    print("exec_time = ", (end_time - start_time), 's')

    # for multiprocess as Pool
    print("for multiprocess as Pool")
    start_time = time.time()
    with Mlp.Pool(5) as pool_proc:   # pool of 5 process
        pool_proc.map(factorize, [128, 255, 99999, 10651060])
    end_time = time.time()
    print("exec_time = ", (end_time - start_time), 's')

    # exit func for visibility result in cmd.exe
    while True:
        exit_code = input("Enter Q for end program\n")
        if exit_code == 'Q' or exit_code == 'q':
            break
