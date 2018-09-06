import logging
import time

from refactor.query_testing_back_end.django.django_wrapper.ClauseWrapper import HypothesisWrapper, ClauseWrapper
from refactor.query_testing_back_end.django.django_wrapper.c_library import lib_django

__matchingV11 = lib_django.MatchingV11


# difficult_example_ids = {'e632_0', 'e1205_2', 'e9734_0', 'e3873_1', 'e8627_1', 'e3664_0', 'e9995_0', 'e3876_3',
#                          'e9332_1', 'e92_0', 'e318_1', 'e5746_2', 'e855_1', 'e92_2', 'e396_0', 'e8162_1', 'e8694_1',
#                          'e5106_2', 'e8162_0', 'e4786_0', 'e9596_2', 'e314_1', 'e8983_1', 'e8983_2', 'e8798_2',
#                          'e5637_0', 'e6905_2', 'e3792_0', 'e1205_0', 'e5259_0', 'e9995_1', 'e1205_1', 'e6756_2',
#                          'e396_2', 'e318_2', 'e8798_1', 'e3395_2', 'e8694_2', 'e9167_0', 'e4371_1', 'e9734_2',
#                          'e3792_2', 'e314_0', 'e5072_2', 'e4371_2'}


def check_subsumption(hypothesis_wrapper: HypothesisWrapper, clause_wrapper: ClauseWrapper, log=False, log_indent=''):
    hypothesis = hypothesis_wrapper.hypothesis
    clause = clause_wrapper.clause

    # if str(clause_wrapper.clause_id) in difficult_example_ids:
    #     snapshot_before_slow_check = tracemalloc.take_snapshot()

    start_time = time.time()
    # TODO: Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
    result = __matchingV11(hypothesis, clause)
    end_time = time.time()
    run_time_sec = end_time - start_time
    run_time_ms = 1000.0 * run_time_sec
    # if result:
    #     print("Positive matching\n")
    # else:
    #     print("Negative matching\n")
    result = bool(result)

    # if str(clause_wrapper.clause_id) in difficult_example_ids:
    #     snapshot_after_slow_check = tracemalloc.take_snapshot()
    #     top_stats = snapshot_after_slow_check.compare_to(snapshot_before_slow_check, 'lineno')
    #     logging.info("+++ stats for " + str(clause_wrapper.clause_id) + " +++")
    #
    #     for stat in top_stats[:10]:
    #         logging.info(stat)

    if log:
        logging.info(
            log_indent + "example: "+ str(clause_wrapper.clause_id) + ", " +
            log_indent + "subsumption: " + str(result) + ", " +
            log_indent + "runtime: " + str(run_time_ms) + " ms" + "\n" +
            log_indent + '--------------------------------------------------------------------------'
        )

    return result, run_time_ms
