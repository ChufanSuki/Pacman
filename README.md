## Pacman
[![codecov](https://codecov.io/gh/ChufanSuki/Pacman/branch/main/graph/badge.svg?token=K2E1RDMLTW)](https://codecov.io/gh/ChufanSuki/Pacman)
![DOCS](https://github.com/ChufanSuki/Pacman/actions/workflows/docs.yml/badge.svg)
![CI](https://github.com/ChufanSuki/Pacman/actions/workflows/ci.yml/badge.svg)
![build](https://github.com/ChufanSuki/Pacman/actions/workflows/build.yml/badge.svg)
![pre-commit](https://github.com/ChufanSuki/Pacman/actions/workflows/pre-commit.yml/badge.svg)

This project is only for education purpose and not for production.
See https://chufansuki.github.io/Pacman/ for doc.

### Related Repo
- https://github.com/ChufanSuki/DCOP for documenting dcop algos
- https://github.com/ChufanSuki/DCOPGenerator for generating xml problem

### Reference:
- https://github.com/andry91/Max_Sum_Python
- https://github.com/houhashv/DCOP
- https://github.com/chiragvartak/dpop

### Example

`python dcop_cli.py solve --algo dpop graph_coloring.yaml`

`python dcop_cli.py --timeout 3 solve --algo mgm graph_coloring.yaml`

`python dcop_cli.py  --output results.json solve --algo dpop graph_coloring.yaml`

`python dcop_cli.py graph --graph factor_graph --display graph_coloring.yaml`

```shell
python dcop_cli.py solve --algo mgm --algo_params stop_cycle:20 \
--collect_on cycle_change --run_metric ./metrics.csv \
graph_coloring_50.yaml
```
```shell
python dcop_cli.py solve --algo mgm --algo_params stop_cycle:20 \
             --collect_on cycle_change \
             --run_metric ./metrics_cycle.csv \
             graph_coloring_50.yaml
```

```shell
python dcop_cli.py -v 2 solve --algo dpop graph_coloring.yaml
```

```shell
python dcop_cli.py --log log.conf orchestrator \
--algo maxsum --algo_params damping:0.9 \
--distribution heur_comhost \
--scenario scenario_2.yaml \
graph_coloring_20.yaml

python dcop_cli.py agent --names a000 a001 a002 a003 a004 a005 a006 a007 a008 a009 a010 \
  a011 a012 a013 a014 a015 a016 a017 a018 a019 a020 \
   -p 9001 --orchestrator 127.0.0.1:9000 --uiport 10001
```


