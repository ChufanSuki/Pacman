
"""
.. _pacman_commands_consolidate:

pacman consolidate
==================

``pacman consolidate`` extract main statistics from a result file.

Synopsis
--------

::

  pacman consolidate <result_file>


Description
-----------

extracting
 extract end metrics from a json result output file.
 produces a csv line, which can be appended to a file

sampling
 takes a run time metrics files, produced with the 'value_change' mode, and
 generate a sample run time metric file


average
 takes a csv file

"""
import csv
import glob
import logging
import json
import os

from typing import List

from pacman.commands.distribute import (
    load_algo_module,
    load_distribution_module,
    load_graph_module,
)
from pacman.dcop.yamldcop import load_dcop_from_file
from pacman.distribution.yamlformat import load_dist_from_file

logger = logging.getLogger("pacman.cli.consolidate")


def set_parser(subparsers):
    parser = subparsers.add_parser(
        "consolidate", help="Various utilities to consolidate data"
    )
    parser.set_defaults(func=run_cmd)

    parser.add_argument("files", type=str, nargs="+", help="file(s)")

    parser.add_argument(
        "--solution",
        action="store_true",
        default=False,
        help="Extract end solution metrics from a json output file",
    )

    parser.add_argument(
        "--distribution_cost",
        type=str,
        default=None,
        help="Distribution file",
    )

    parser.add_argument(
        "--algo",
        type=str,
        default=None,
        help="DCOP algorithm",
    )


    parser.add_argument(
        "--average",
        action="store_true",
        default=False,
        help="compute average result from a json output file",
    )

    parser.add_argument(
        "--replace_output",
        action="store_true",
        default=False,
        help="Replace output file instead of appending",
    )



def run_cmd(args):

    if args.output and args.replace_output:
        if os.path.exists(args.output):
            os.remove(args.output)

    if args.solution:
        files = args.files
        if args.output:
            if not os.path.exists(args.output):
                with open(args.output, mode="w") as output_file:
                    csv_writer = csv.writer(output_file)
                    csv_writer.writerow(
                        ["time", "cost", "cycle", "msg_count", "msg_size", "status"]
                    )
            with open(args.output, mode="a", newline="") as output_file:
                extract(files, output_file)
        else:
            target = extract(files, WriterTarget())
            print(target.writen)
    elif args.distribution_cost:
        files = args.files
        if args.output:
            if not os.path.exists(args.output):
                with open(args.output, mode="w") as output_file:
                    csv_writer = csv.writer(output_file)
                    csv_writer.writerow(["dcop", "distribution", "cost", "hosting", "communication"])
            with open(args.output, mode="a", newline="") as output_file:
                distribution_cost(files, args.distribution_cost, args.algo,  output_file)
        else:
            target = distribution_cost(files, args.distribution_cost, args.algo, WriterTarget())
            print("dcop, distrib, cost, hosting, communication")
            print(target.writen)


def distribution_cost(
    dcop_files: List[str], distribution_file, algo, target
):
    logger.debug(f"analyse file {dcop_files}")

    dcop = load_dcop_from_file(dcop_files)
    path_glob = os.path.abspath(os.path.expanduser(distribution_file))
    distribution_files = sorted(glob.iglob(path_glob))
    for distribution_file in distribution_files:

        try:
            cost, comm, hosting = single_distrib_costs(
                dcop, distribution_file, algo
            )

            csv_writer = csv.writer(target)
            csv_writer.writerow([dcop_files[0], distribution_file, cost, hosting, comm])
        except:
            pass
    return target


def single_distrib_costs(dcop, distribution_file, algo):
    # load files
    distribution = load_dist_from_file(distribution_file)

    # load modules
    algo_module = load_algo_module(algo)
    dist_module = load_distribution_module("ilp_compref")
    graph_module = load_graph_module(algo_module.GRAPH_TYPE)

    cg = graph_module.build_computation_graph(dcop)
    computation_memory = algo_module.computation_memory
    communication_load = algo_module.communication_load

    cost, comm, hosting = dist_module.distribution_cost(
        distribution,
        cg,
        dcop.agents.values(),
        computation_memory=computation_memory,
        communication_load=communication_load,
    )
    return cost, comm, hosting


def extract(files: List[str], target):

    for file in files:
        logger.debug(f"analyse file {file}")
        with open(file, mode="r") as f:

            data_json = json.load(f)
            data = [
                data_json["time"],
                data_json["cost"],
                data_json["cycle"],
                data_json["msg_count"],
                data_json["msg_size"],
                data_json["status"],
            ]
            csv_writer = csv.writer(target)
            csv_writer.writerow(data)

    return target


class WriterTarget:

    writen: str = ""

    def write(self, s):
        self.writen += s
