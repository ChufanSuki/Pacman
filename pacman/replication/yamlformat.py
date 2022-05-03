


"""
Saving and loading replica distribution to and from yaml.


"""
import yaml

from pacman.replication.objects import ReplicaDistribution


def load_replica_dist_from_file(filename: str) -> ReplicaDistribution:
    with open(filename, mode='r', encoding='utf-8') as f:
        content = f.read()
    if content:
        return load_replica_dist(content)

def load_replica_dist(dist_str: str) -> ReplicaDistribution:
    loaded = yaml.load(dist_str, Loader=yaml.FullLoader)

    if 'replica_dist' not in loaded:
        raise ValueError('Invalid replica distribution file')

    loaded_dist = loaded['replica_dist']

    return ReplicaDistribution(loaded_dist)

