
import json
import unittest
from subprocess import STDOUT, check_output, CalledProcessError

from test.instances.utils import instance_path


class SimpleSecpDCOP1(unittest.TestCase):

    def check_results(self, results):
        # No convergence detection for now, always stop on timeout
        self.assertEqual(results['status'], 'TIMEOUT')
        assignment = results['assignment']
        self.assertEqual(assignment['l1'], 0)
        self.assertEqual(assignment['l2'], 3)
        self.assertEqual(assignment['l3'], 4)
        self.assertEqual(assignment['m1'], 3)

    def test_maxsum_ilp_fgdp(self):
        result = run_solve('maxsum', 'ilp_fgdp', 'secp_simple1.yaml', 5)
        print(result)
        self.check_results(result)

    def test_maxsum_ilp_fgdp_process(self):
        result = run_solve('maxsum', 'ilp_fgdp', 'secp_simple1.yaml', 5,
                           'process')
        self.check_results(result)

    def test_maxsum_adhoc(self):
        result = run_solve('maxsum', 'adhoc', 'secp_simple1.yaml', 5)
        self.check_results(result)

    def test_maxsum_adhoc_process(self):
        result = run_solve('maxsum', 'adhoc', 'secp_simple1.yaml', 5,
                           'process')
        self.check_results(result)

    def test_maxsum_oneagent(self):
        # Must fail : there is not enough agent for the oneagent
        # distribution method.
        self.assertRaises(CalledProcessError, run_solve,
                          'maxsum', 'oneagent', 'secp_simple1.yaml', 5)

    @unittest.skip
    # Skip the test, adhoc requires an algorithm with computation footprint
    # and dcop does not have it
    def test_dpop_adhoc(self):
        result = run_solve('dpop', 'adhoc', 'secp_simple1.yaml', 5)
        self.check_results(result)

    @unittest.skip
    # Skip the test, adhoc requires an algorithm with computation footprint
    # and dcop does not have it
    def test_dpop_adhoc_process(self):
        result = run_solve('dpop', 'adhoc', 'secp_simple1.yaml', 5, 'process')
        self.check_results(result)

    def test_dsa_adhoc(self):
        result = run_solve('dsa', 'adhoc', 'secp_simple1.yaml', 5)
        # Do not really check the results, dsa performs poorly on this pb
        # self.check_results(result)

    def test_dsa_adhoc_process(self):
        result = run_solve('dsa', 'adhoc', 'secp_simple1.yaml', 5, 'process')
        # Do not really check the results, dsa performs poorly on this pb
        # self.check_results(result)


class GraphColoring1(unittest.TestCase):

    def check_results(self, results, status='TIMEOUT'):
        # No convergence detection for now, always stop on timeout
        self.assertEqual(results['status'], status)
        assignment = results['assignment']
        self.assertEqual(assignment['v1'], 'R')
        self.assertEqual(assignment['v2'], 'G')
        self.assertEqual(assignment['v3'], 'R')

    def test_maxsum_ilp_fgdp(self):
        result = run_solve('maxsum', 'ilp_fgdp', 'graph_coloring1.yaml', 5)
        self.check_results(result)

    def test_maxsum_adhoc(self):
        result = run_solve('maxsum', 'adhoc', 'graph_coloring1.yaml', 1)
        self.check_results(result)

    def test_maxsum_adhoc_process(self):
        result = run_solve('maxsum', 'adhoc', 'graph_coloring1.yaml', 3,
                           'process')
        self.check_results(result)

    def test_maxsum_oneagent(self):
        result = run_solve('maxsum', 'oneagent', 'graph_coloring1.yaml', 1)
        self.check_results(result)

    def test_maxsum_oneagent_process(self):
        result = run_solve('maxsum', 'oneagent', 'graph_coloring1.yaml', 3,
                           'process')
        self.check_results(result)

    @unittest.skip
    # Skip the test, adhoc requires an algorithm with computation footprint
    # and dcop does not have it
    def test_dpop_adhoc(self):
        result = run_solve('dpop', 'adhoc', 'graph_coloring1.yaml', 1)
        self.check_results(result)

    @unittest.skip
    # Skip the test, adhoc requires an algorithm with computation footprint
    # and dcop does not have it
    def test_dpop_adhoc_process(self):
        result = run_solve('dpop', 'adhoc', 'graph_coloring1.yaml', 3,
                           'process')
        self.check_results(result)

    def test_dpop_oneagent(self):
        result = run_solve('dpop', 'oneagent', 'graph_coloring1.yaml', 2)
        self.check_results(result, 'FINISHED')

    def test_dpop_oneagent_process(self):
        result = run_solve('dpop', 'oneagent', 'graph_coloring1.yaml', 3,
                           'process')
        self.check_results(result, 'FINISHED')

    def test_dpop_ilp_fgdp(self):
        # ILP-FGDP does not work for dpop, it should return an error
        self.assertRaises(CalledProcessError, run_solve,
                          'dpop', 'ilp_fgdp', 'graph_coloring1.yaml', 1)

    def test_dsa_adhoc(self):
        result = run_solve('dsa', 'adhoc', 'graph_coloring1.yaml', 1)
        # Do not really check the results, dsa often don't find the best
        # solution this pb
        # self.check_results(result)

    def test_dsa_adhoc_process(self):
        result = run_solve('dsa', 'adhoc', 'graph_coloring1.yaml', 3,
                           'process')
        # Do not really check the results, dsa often don't find the best
        # solution this pb
        # self.check_results(result)

    def test_dsa_oneagent(self):
        result = run_solve('dsa', 'oneagent', 'graph_coloring1.yaml', 1)
        # Do not really check the results, dsa often don't find the best
        # solution this pb
        # self.check_results(result)

    def test_dsa_oneagent_process(self):
        result = run_solve('dsa', 'oneagent', 'graph_coloring1.yaml', 3,
                           'process')
        # Do not really check the results, dsa often don't find the best
        # solution this pb
        # self.check_results(result)

    def test_dsa_ilp_fgdp(self):
        # ILP-FGDP does not work for dsa, it should return an error
        self.assertRaises(CalledProcessError, run_solve,
                          'dsa', 'ilp_fgdp', 'graph_coloring1.yaml', 1)


class GraphColoring10(unittest.TestCase):

    def check_results(self, results):
        # No convergence detection for now, always stop on timeout
        self.assertEqual(results['status'], 'TIMEOUT')
        assignment = results['assignment']
        self.assertEqual(results['cost'], 0)

    def test_mgm_adhoc(self):
        result = run_solve('mgm', 'adhoc', 'graph_coloring_10_4_15_0.1.yml', 2)
        self.check_results(result)

    def test_dpop_oneagent(self):
        results = run_solve('dpop', 'oneagent', 'graph_coloring_10_4_15_0.1.yml', 3)
        self.assertEqual(results['status'], 'FINISHED')

        assignment = results['assignment']
        self.assertEqual(results['cost'], 0)

class GraphColoringCsp(unittest.TestCase):

    def check_results(self, results):
        # No convergence detection for now, always stop on timeout
        self.assertEqual(results['status'], 'FINISHED')
        assignment = results['assignment']
        self.assertEqual(results['cost'], 0)

    def test_dba_adhoc(self):
        result = run_solve('dba', 'adhoc', 'graph_coloring_csp.yaml', 3)
        self.check_results(result)

    def test_dba_adhoc_process(self):
        result = run_solve('dba', 'adhoc', 'graph_coloring_csp.yaml', 3,
                           'process')
        self.check_results(result)

    def test_dba_oneagent(self):
        result = run_solve('dba', 'oneagent', 'graph_coloring_csp.yaml', 3)
        self.check_results(result)

    def test_dba_oneagent_params(self):
        result = run_solve('dba', 'oneagent', 'graph_coloring_csp.yaml', 3,
                           algo_params=['infinity:10000', 'max_distance:3'])
        self.check_results(result)

    def test_dba_oneagent_params_process(self):
        result = run_solve('dba', 'oneagent', 'graph_coloring_csp.yaml', 4,
                           algo_params=['infinity:10000', 'max_distance:3'],
                           mode='process')
        self.check_results(result)


def run_solve(algo, distribution, filename, timeout: int, mode='thread',
              algo_params=''):
    filename = instance_path(filename)
    param_str = ''
    for p in algo_params:
        param_str += ' --algo_param '+ p
    cmd = 'pacman -v 0 -t {timeout} solve -a {algo} {params} -d {' \
          'distribution} ' \
          '-m {mode} ' \
          '{file}'.format(timeout=timeout,
                          algo=algo,
                          params=param_str,
                          distribution=distribution,
                          file=filename,
                          mode=mode)
    extra = 4 if mode == 'thread' else 5
    print("Running command ", cmd)
    output = check_output(cmd, stderr=STDOUT, timeout=timeout+extra,
                          shell=True)
    print(output)
    res = {}
    try:
        res = json.loads(output.decode(encoding='utf-8'))
    except Exception as e:
        print(e)
    return res
