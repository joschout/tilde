import statistics
import timeit

import gc

times = []

for i in range(0, 10):

    start = timeit.default_timer()
    import mai_version.test_datasets.bongard_keys

    gc.collect()
    end = timeit.default_timer()
    times.append(end - start)

print("average duration:", statistics.mean(times), "seconds")