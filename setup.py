"""Setup for imitation: a reward and imitation learning library."""

from setuptools import find_packages, setup

import pacman  # pytype: disable=import-error

TESTS_REQUIRE = [
    "coverage",
    "codecov",
    "flake8",
    "pytest",
    "pytest-cov",
]
DOCS_REQUIRE = [
    "sphinx",
    "sphinx-autodoc-typehints",
    "sphinx-rtd-theme",
    "sphinxcontrib-napoleon",
]


def get_readme() -> str:
    """Retrieve content from README."""
    with open("README.md") as f:
        return f.read()


setup(
    name="pacman",
    version=pacman.__version__,
    description="Several dcop algo implementation.",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    author="Chufan Chen",
    python_requires=">=3.7.0",
    packages=find_packages(),
    install_requires=[
        "pulp",
        "numpy",
        "networkx",
        "pyyaml",
        "requests",
        "websocket-server",
        "tqdm",
        "matplotlib"
    ],
    tests_require=TESTS_REQUIRE,
    extras_require={
        "test": TESTS_REQUIRE,
        "docs": DOCS_REQUIRE,
    },
    url="https://github.com/chufansuki/pacman",
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
