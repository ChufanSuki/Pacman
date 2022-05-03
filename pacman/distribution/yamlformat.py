
"""
Saving and loading distribution to and from yaml.


"""
import yaml

from pacman.distribution.objects import Distribution


def load_dist_from_file(filename: str) -> Distribution:
    with open(filename, mode='r', encoding='utf-8') as f:
        content = f.read()
    if content:
        return load_dist(content)

def load_dist(dist_str: str) -> Distribution:
    loaded = yaml.load(dist_str, Loader=yaml.FullLoader)

    if 'distribution' not in loaded:
        raise ValueError('Invalid distribution file')

    loaded_dist = loaded['distribution']

    return Distribution(loaded_dist)

