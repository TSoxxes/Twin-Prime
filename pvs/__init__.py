"""
PVS - Prime Vector Space
========================

A library for exploring prime number distribution using geometric and
computational number theory concepts, particularly inspired by the
work of Goldston, Pintz, and Yıldırım (GPY) on small gaps between primes.

Modules:
  algebra:  Provides algebraic structures and operations (currently a placeholder).
  cli:      Command-line interface for accessing PVS functionalities.
  config:   Configuration management (currently a placeholder).
  geometry: Tools for constructing prime vectors and related geometric objects,
            like the Sieve of Eratosthenes.
  io:       Input/output utilities, especially for handling large numerical data
            (currently a placeholder, some IO in cli.py).
  weights:  Functions for calculating weights used in sieve methods, such as
            GPY weights.
"""

# Version of the pvs library
__version__ = "0.1.0"

# Expose key functions or classes at the package level if desired
# For example:
# from .geometry import build_prime_vector, sieve_of_eratosthenes
# from .weights import gpy_weight

# Or, to keep the namespace cleaner, users can import from submodules:
# import pvs.geometry
# import pvs.weights

# For now, let's keep it simple and not expose anything directly at the top level,
# encouraging submodule imports.

# Placeholder for global configurations or initializations if needed in the future.
# print("PVS package initialized.")
