"""Compute positions of various secondary source distributions."""

import numpy as np
from . import util


def linear(N, dx, center=[0, 0, 0], n0=[1, 0, 0]):
    """Linear secondary source distribution."""
    center = np.squeeze(np.asarray(center, dtype=np.float64))
    positions = np.zeros((N, 3))
    positions[:, 1] = (np.arange(N) - N / 2 + 1 / 2) * dx
    directions = np.tile([1, 0, 0], (N, 1))
    positions, directions = _rotate_array(positions, directions, [1, 0, 0], n0)
    positions += center

    return positions, directions


def circular(N, R, center=[0, 0, 0]):
    """Circular secondary source distribution parallel to the xy-plane."""
    center = np.squeeze(np.asarray(center, dtype=np.float64))
    positions = np.tile(center, (N, 1))
    alpha = np.linspace(0, 2 * np.pi, N, endpoint=False)
    positions[:, 0] += R * np.cos(alpha)
    positions[:, 1] += R * np.sin(alpha)
    directions = np.zeros_like(positions)
    directions[:, 0] = np.cos(alpha + np.pi)
    directions[:, 1] = np.sin(alpha + np.pi)
    return positions, directions


def rectangular(Nx, dx, Ny, dy, center=[0, 0, 0], n0=None):
    """Rectangular secondary source distribution."""

    # left array
    x00, n00 = linear(Ny, dy)
    positions = x00
    directions = n00
    # upper array
    x00, n00 = linear(Nx, dx, center=[Nx/2 * dx, x00[-1, 1] + dy/2, 0],
                      n0=[0, -1, 0])
    positions = np.concatenate((positions, x00))
    directions = np.concatenate((directions, n00))
    # right array
    x00, n00 = linear(Ny, dy, center=[x00[-1, 0] + dx/2, 0, 0], n0=[-1, 0, 0])
    x00 = np.flipud(x00)
    positions = np.concatenate((positions, x00))
    directions = np.concatenate((directions, n00))
    # lower array
    x00, n00 = linear(Nx, dx, center=[Nx/2 * dx, x00[-1, 1] - dy/2, 0],
                      n0=[0, 1, 0])
    positions = np.concatenate((positions, x00))
    directions = np.concatenate((directions, n00))
    # shift array to center
    positions -= np.asarray([Nx/2 * dx, 0, 0])
    # rotate array
    if n0 is not None:
        positions, directions = _rotate_array(positions, directions,
                                              [1, 0, 0], n0)
    # shift array to desired positions
    positions += np.asarray(center)

    return positions, directions


def _rotate_array(x0, n0, n1, n2):
    """Rotate secondary sources from n1 to n2."""
    R = util.rotation_matrix(n1, n2)
    x0 = np.inner(x0, R)
    n0 = np.inner(n0, R)
    return x0, n0
