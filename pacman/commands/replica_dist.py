

"""
.. _pacman_commands_replica_dist:

pacman replica_dist
===================

Distributing computation replicas

Synopsis
--------

::

  pacman orchestrator


Description
-----------

To distribute computations' replicas, one need :

* a computation graph
  => we need to known the list of computations and which computation is
  communicating with which (edges in the computation graph)

* computations distribution
  => we could pass a distribution method and  compute it or directly pass a
  distribution file ( agent -> [computations])

* computations weight ans msg load
  => these depends on the dcop algorithm we are going to use

* route costs & agents preferences
  => these are given in the dcop definition yaml file


Options
-------

TODO


Examples
--------

Passing the computation distribution::

  pacman replica_dist -r dist_ucs -k 3
                      -a dsa --distribution dist_graphcoloring.yml
                      graph_coloring_10_4_15_0.1.yml



"""

import logging
import sys
import multiprocessing
import time
import threading
import traceback
from importlib import import_module
from threading import Timer

import yaml

from pacman.algorithms import list_available_algorithms, load_algorithm_module
from pacman.commands._utils import build_algo_def
from pacman.dcop.yamldcop import load_dcop_from_file
from pacman.distribution.yamlformat import load_dist_from_file
from pacman.infrastructure.run import run_local_thread_dcop, run_local_process_dcop

logger = logging.getLogger("pacman.cli.replica_dist")


def set_parser(subparsers):

    algorithms = list_available_algorithms()
    logger.debug("Available DCOP algorithms %s", algorithms)

    parser = subparsers.add_parser("replica_dist", help="distribution replicas ")
    parser.set_defaults(func=run_cmd)
    parser.set_defaults(on_timeout=on_timeout)
    parser.set_defaults(on_force_exit=on_force_exit)

    parser.add_argument("dcop_files", type=str, nargs="+", help="dcop file")

    parser.add_argument(
        "-k", "--ktarget", required=True, type=int, help="Requested resiliency level"
    )
    parser.add_argument(
        "-r",
        "--replication",
        required=True,
        type=str,
        choices=["dist_ucs", "dist_ucs_hostingcosts"],
        help="Replication distribution algorithm",
    )

    # Distribution given as a file
    parser.add_argument(
        "-d",
        "--distribution",
        type=str,
        help="File containing the distribution of computations " "on the agents",
    )
    # algo used when running the dcop
    parser.add_argument(
        "-a",
        "--algo",
        choices=algorithms,
        help="Algorithm for solving the dcop, necessary to "
        "know the footprint of computation when "
        "distributing replicas on agents",
    )

    parser.add_argument(
        "-m",
        "--mode",
        default="thread",
        choices=["thread", "process"],
        help="run agents as threads or processes",
    )


orchestrator = None


def run_cmd(args, timer: Timer = None, timeout= None):
    logger.debug("Distribution replicas : %s", args)
    global orchestrator

    # global dcop
    logger.info("loading dcop from {}".format(args.dcop_files))
    dcop = load_dcop_from_file(args.dcop_files)

    try:
        algo_module = load_algorithm_module(args.algo)
        algo = build_algo_def(
            algo_module, args.algo, dcop.objective, []
        )  # FIXME : algo params needed?

        graph_module = import_module(
            "pacman.computations_graph.{}".format(algo_module.GRAPH_TYPE)
        )
        logger.info("Building computation graph ")
        cg = graph_module.build_computation_graph(dcop)
        logger.info("Computation graph : %s", cg)

    except ImportError:
        _error(
            "Could not find module for algorithm {} or graph model "
            "for this algorithm".format(args.algo)
        )

    logger.info("loading distribution from {}".format(args.distribution))
    distribution = load_dist_from_file(args.distribution)

    INFINITY = 10000  # FIXME should not be mandatory

    global orchestrator
    if args.mode == "thread":
        orchestrator = run_local_thread_dcop(
            algo, cg, distribution, dcop, INFINITY, replication=args.replication
        )
    elif args.mode == "process":

        # Disable logs from agents, they are in other processes anyway
        agt_logs = logging.getLogger("pacman.agent")
        agt_logs.disabled = True

        # When using the (default) 'fork' start method, http servers on agent's
        # processes do not work (why ?)
        multiprocessing.set_start_method("spawn")
        orchestrator = run_local_process_dcop(
            algo, cg, distribution, dcop, INFINITY, replication=args.replication
        )

    try:
        orchestrator.deploy_computations()
        start_t = time.time()
        orchestrator.start_replication(args.ktarget)
        orchestrator.wait_ready()
        # print(f" Replication Metrics {orchestrator.replication_metrics()}")
        metrics = orchestrator.replication_metrics()
        msg_count, msg_size = 0,0
        for a in metrics:
            msg_count +=  metrics[a]["count_ext_msg"]
            msg_size +=  metrics[a]["size_ext_msg"]
        # print(f" Count: {msg_count} - Size {msg_size}")
        duration = time.time() - start_t
        if timer:
            timer.cancel()
        rep_dist = {
            c: list(hosts) for c, hosts in orchestrator.mgt.replica_hosts.items()
        }
        orchestrator.stop_agents(5)
        orchestrator.stop()
        result = {
            "inputs": {
                "dcop": args.dcop_files,
                "algo": args.algo,
                "replication": args.replication,
                "k": args.ktarget,
            },
            "metrics": {
                "duration": duration,
                "msg_size": msg_size,
                "msg_count": msg_count,
            },
            "replica_dist": rep_dist,
        }
        result["inputs"]["distribution"] = args.distribution
        if args.output is not None:
            with open(args.output, encoding="utf-8", mode="w") as fo:
                fo.write(yaml.dump(result))
        else:
            print(yaml.dump(result))
        sys.exit(0)

        # TODO : retrieve and display replica distribution
        # Each agent should send back to the orchestrator the agents hosting
        # the replicas for each of it's computations
    except Exception as e:
        orchestrator.stop_agents(5)
        orchestrator.stop()
        _error("ERROR", e)


def on_timeout():
    _error("TIMEOUT")


def on_force_exit(sig, frame):
    for th in threading.enumerate():
        print(th)
        traceback.print_stack(sys._current_frames()[th.ident])
        print()
    _error("STOPPED")


def _error(msg, e=None):
    print("Error: {}".format(msg))
    if e is not None:
        print(e)
        tb = traceback.format_exc()
        print(tb)
    sys.exit(2)
