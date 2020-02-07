"""Determines if a pure state is a product vector."""
from typing import List, Union
import numpy as np

from toqito.states.schmidt_decomposition import schmidt_decomposition


def is_product_vector(vec: np.ndarray, dim: Union[int, List[int]]) -> bool:
    """
    """
    eps = np.finfo(float).eps
    lv = len(vec)

    if dim is None:
        dim = np.round(np.sqrt(lv))

    # Allow the user to enter a single number for dim.
    if isinstance(dim, int):
        num_sys = 1
    else:
        num_sys = len(dim)

    if num_sys == 1:
        dim = np.array([dim, lv/dim])
        if np.abs(dim[1] - np.round(dim[1])) >= 2 * lv * eps:
            msg = """
                InvalidDim: The value of `dim` must evenly divide `len(vec)`.
                Please provide a `dim` array containing the dimensions of the
                subsystems.
            """
            raise ValueError(msg)
        dim[1] = np.round(dim[1])
        num_sys = 2

    # If there are only two subsystems, just use the Schmidt decomposition.
    if num_sys == 2:
        singular_vals, u_mat, vt_mat = schmidt_decomposition(vec, dim, 2)
        ipv = (singular_vals[1] <= np.prod(dim) * np.spacing(singular_vals[0]))

        # Provide this even if not requested, since it is needed if this
        # function was called as part of its recursive algorithm (see below)
        pass