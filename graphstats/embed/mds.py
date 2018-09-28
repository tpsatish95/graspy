import numpy as np
from scipy.sparse.linalg import svds
from sklearn.base import BaseEstimator

from .svd import selectSVD


def _get_centering_matrix(n):
    """
    Compute the centering matrix
    """
    return np.identity(n) - (1 / n) * np.ones((n, n))


class ClassicalMDS(BaseEstimator):
    """
    Classical multidimensional scaling (cMDS).

    cMDS  seeks a low-dimensional representation of the data in
    which the distances respect well the distances in the original
    high-dimensional space.

    Parameters
    ----------
    n_components : int, or None
        Number of components to keep. If None, then it will run
        ``dimselect`` to find the optimal embedding dimension.

    Attributes
    ----------
    components_ : array, shape (n_components, n_features)
        Principal axes in feature space.

    singular_values_ : array, shape (n_components,)
        The singular values corresponding to each of the selected components.

    n_components_ : int
        Equals the parameter n_components, or n_features if n_components
        is None.

    See Also
    --------
    graphstats.embed.dimselect
    """

    def __init__(self, n_components):
        self.n_components = n_components

    def fit(self, X):
        """
        Fit the model with X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_samples)
            Precomputed Euclidean dissimilarity matrix.
        """
        # Handle n_components==None
        if self.n_components is None:
            # TODO: use dimselect here
            n_components = min(X.shape) - 1
        else:
            n_components = self.n_components

        n_vertices = X.shape[0]

        J = _get_centering_matrix(n_vertices)
        B = J.dot(X**2).dot(J)
        B *= -0.5

        U, V, D = selectSVD(B, k=n_components)

        self.components_ = U
        self.singular_values_ = D

        return self

    def fit_transform(self, X):
        """
        Fit the model with X and apply the dimensionality reduction on X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_samples)
            Precomputed Euclidean dissimilarity matrix.
        """
        self.fit(X)

        X_new = np.dot(self.components_, np.diag(self.singular_values_**0.5))

        return X_new