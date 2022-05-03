

from typing import Iterable, Optional, Tuple, List, Set

Node = str
Path = Tuple[Node, ...]


def head(path) -> Optional[Node]:
    """
    Returns
    -------
    The first element of the path of None if the path is empty
    """
    try:
        return path[0]
    except IndexError:
        return None


def last(path) -> Optional[Node]:
    """

    Returns
    -------
    The last element of the path, or None if the path is empty
    """
    try:
        return path[-1]
    except IndexError:
        return None


def before_last(path):
    """

    Returns
    -------
    The element before the last element in the path

    Raises
    ------
    IndexError if the path has 1 or less elements
    """
    return path[-2]


PathsTable = List[Tuple[float, Path]]


def remove_path(paths: PathsTable, path: Path) -> PathsTable:
    """
     Remove a path from a list of paths. Maintains ordering

    Parameters
    ----------
    paths
    path

    Returns
    -------

    """
    to_remove = [(c, p) for c, p in paths if p == path]
    for item in to_remove:
        paths.remove(item)
    return paths


def cheapest_path_to(target: Node, paths: PathsTable) -> Tuple[float, Path]:
    """
    Search the cheapest path and its costs in `paths` that ends at `target`.

    Parameters
    ----------
    target: Node
        The end node to look for
    paths: dict of path, float
        A dict of known paths with their costs

    Returns
    -------
    Tuple[float, Path]
        A Tuple containing the cheapest cost and the corresponding path. If
        `paths` contains no path ending at target, return an infinite cost with
        an empty path.

    :return:
    """
    for cost, p in paths:
        if p[-1] == target:
            return cost, p
    return float("inf"), ()


def affordable_path_from(prefix: Path, max_path_cost: float, paths: PathsTable):
    # filtered = []
    plen = len(prefix)
    for cost, path in paths:
        if path[:plen] == prefix and (cost - max_path_cost) <= 0.0001:
            yield path[plen:]
            # filtered.append((cost, path[plen:]))
    # return filtered


def filter_missing_agents_paths(
    paths: PathsTable, removed_agents: Set
) -> PathsTable:
    """
    Filters out all paths passing through an agent that is not
    available any more.

    Parameters
    ----------
    paths: PathsTable
        known paths with their associated costs
    removed_agents:
        names of removed agents

    Returns
    -------
    A new PathsTable with only valid paths.

    """
    filtered = []
    for cost, path in paths:
        missing = False
        for elt in path:
            if elt in removed_agents:
                missing = True
                break
        if missing:
            continue
        filtered.append((cost, path))
    return filtered
