import unittest
import graphstats as gs
import numpy as np
import networkx as nx
from graphstats.simulations.simulations import *
from graphstats.utils.utils import is_symmetric, is_loopless


def remove_diagonal(A):
    # indices of A
    Aind = np.ravel_multi_index(np.indices(A.shape), A.shape)
    # indices of the diagonal
    eind = np.ravel_multi_index(np.where(np.eye(A.shape[1])), A.shape)
    # set difference of A indices and identity
    dind = np.unravel_index(np.setdiff1d(Aind, eind), A.shape)
    return(A[dind])

class Test_ER(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.n = 20
        cls.M = 45
        cls.p = 0.2

    def test_ernm(self):
        A = er_nm(self.n, self.M)
        # symmetric, so summing will give us twice the ecount of
        # the full adjacency matrix
        self.assertTrue(A.sum() == 2*self.M)
        self.assertTrue(A.shape == (self.n, self.n))

    def test_ernp(self):
        np.random.seed(123456)
        A = er_np(self.n, self.p)
        # symmetric, so summing will give us twice the ecount of
        # the full adjacency matrix
        dind = remove_diagonal(A)
        self.assertTrue(np.isclose(dind.sum()/float(len(dind)),
            self.p, atol=0.02))
        self.assertTrue(A.shape == (self.n, self.n))


class Test_ZINM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.n = 20
        cls.M = 120
        cls.wt = np.random.normal
        cls.mean = 2
        cls.std = 1

    def test_loop_directed(self):
        np.random.seed(12345)
        Abin = zi_nm(self.n, self.M, directed=True, loops=True)
        Awt = zi_nm(self.n, self.M, directed=True, loops=True, wt=self.wt,
            loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        # sum of nonzero entries and correct for the fact that the diagonal
        # is part of the model now
        self.assertTrue(Abin.sum() == self.M)
        self.assertTrue((Awt != 0).sum() == self.M)


        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(Awt[Awt != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(Awt[Awt != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertFalse(is_symmetric(Abin))
        self.assertFalse(is_symmetric(Awt))
        self.assertFalse(is_loopless(Abin))
        self.assertFalse(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass

    def test_noloop_directed(self):
        np.random.seed(12345)
        Abin = zi_nm(self.n, self.M, directed=True)
        Awt = zi_nm(self.n, self.M, wt=self.wt, directed=True,
            loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        self.assertTrue(Abin.sum() == self.M)
        self.assertTrue((Awt != 0).sum() == self.M)

        dind = remove_diagonal(Awt)
        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(dind[dind != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(dind[dind != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertFalse(is_symmetric(Abin))
        self.assertFalse(is_symmetric(Awt))
        self.assertTrue(is_loopless(Abin))
        self.assertTrue(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass

    def test_loop_undirected(self):
        np.random.seed(12345)
        Abin = zi_nm(self.n, self.M, loops=True)
        Awt = zi_nm(self.n, self.M, loops=True, wt=self.wt,
            loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        # sum of nonzero entries and correct for the fact that the diagonal
        # is part of the model now
        self.assertTrue(Abin.sum() + np.diag(Abin).sum() == 2*self.M)
        self.assertTrue((Awt != 0).sum() + np.diag(Awt != 0).sum() == 2*self.M)

        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(Awt[Awt != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(Awt[Awt != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertTrue(is_symmetric(Abin))
        self.assertTrue(is_symmetric(Awt))
        self.assertFalse(is_loopless(Abin))
        self.assertFalse(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass


    def test_noloop_undirected(self):
        np.random.seed(12345)
        Abin = zi_nm(self.n, self.M)
        Awt = zi_nm(self.n, self.M, wt=self.wt, loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        self.assertTrue(Abin.sum() == 2*self.M)
        self.assertTrue((Awt != 0).sum() == 2*self.M)

        dind = remove_diagonal(Awt)
        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(dind[dind != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(dind[dind != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertTrue(is_symmetric(Abin))
        self.assertTrue(is_symmetric(Awt))
        self.assertTrue(is_loopless(Abin))
        self.assertTrue(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass


class Test_ZINP(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.n = 50
        cls.p = 0.5
        cls.wt = np.random.normal
        cls.mean = 2
        cls.std = 1

    def test_loop_directed(self):
        np.random.seed(12345)
        Abin = zi_np(self.n, self.p, directed=True, loops=True)
        Awt = zi_np(self.n, self.p, directed=True, loops=True, wt=self.wt,
            loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        # sum of nonzero entries and correct for the fact that the diagonal
        # is part of the model now
        self.assertTrue(np.isclose(Abin.sum()/float(np.prod(Abin.shape)),
            self.p, atol=0.02))
        self.assertTrue(np.isclose((Awt != 0).sum()/float(np.prod(Awt.shape)),
            self.p, atol=0.02))

        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(Awt[Awt != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(Awt[Awt != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertFalse(is_symmetric(Abin))
        self.assertFalse(is_symmetric(Awt))
        self.assertFalse(is_loopless(Abin))
        self.assertFalse(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass

    def test_noloop_directed(self):
        np.random.seed(12345)
        Abin = zi_np(self.n, self.p, directed=True)
        Awt = zi_np(self.n, self.p, wt=self.wt, directed=True,
            loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        dind = remove_diagonal(Abin)
        dindwt = remove_diagonal(Awt)
        self.assertTrue(np.isclose(dind.sum()/float(len(dind)),
            self.p, atol=0.02))
        self.assertTrue(np.isclose((dindwt != 0).sum()/float(len(dindwt)),
            self.p, atol=0.02))

        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(dindwt[dindwt != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(dindwt[dindwt != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertFalse(is_symmetric(Abin))
        self.assertFalse(is_symmetric(Awt))
        self.assertTrue(is_loopless(Abin))
        self.assertTrue(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass

    def test_loop_undirected(self):
        np.random.seed(12345)
        Abin = zi_np(self.n, self.p, loops=True)
        Awt = zi_np(self.n, self.p, loops=True, wt=self.wt,
            loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        self.assertTrue(np.isclose(Abin.sum()/float(np.prod(Abin.shape)),
            self.p, atol=0.02))
        self.assertTrue(np.isclose((Awt != 0).sum()/float(np.prod(Awt.shape)),
            self.p, atol=0.02))
        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(Awt[Awt != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(Awt[Awt != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertTrue(is_symmetric(Abin))
        self.assertTrue(is_symmetric(Awt))
        self.assertFalse(is_loopless(Abin))
        self.assertFalse(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass


    def test_noloop_undirected(self):
        np.random.seed(123)
        Abin = zi_np(self.n, self.p)
        Awt = zi_np(self.n, self.p, wt=self.wt, loc=self.mean, scale=self.std)
        # check that correct number of edges assigned
        dind = remove_diagonal(Abin)
        dindwt = remove_diagonal(Awt)
        self.assertTrue(np.isclose(dind.sum()/float(len(dind)),
            self.p, atol=0.02))
        self.assertTrue(np.isclose((dindwt != 0).sum()/float(len(dindwt)),
            self.p, atol=0.02))

        # check that the nonzero edges have mean self.mean and var self.var
        self.assertTrue(np.isclose(np.mean(dindwt[dindwt != 0]), self.mean,
            atol=0.15))
        self.assertTrue(np.isclose(np.std(dindwt[dindwt != 0]), self.std,
            atol=0.15))

        # check loopless and undirected
        self.assertTrue(is_symmetric(Abin))
        self.assertTrue(is_symmetric(Awt))
        self.assertTrue(is_loopless(Abin))
        self.assertTrue(is_loopless(Awt))

        # check dimensions
        self.assertTrue(Abin.shape == (self.n, self.n))
        self.assertTrue(Awt.shape == (self.n, self.n))
        pass


class Test_WSBM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 60 vertex graph w one community having 20 and another
        # w 40 vertices
        cls.n = [50, 70]
        cls.vcount = np.cumsum(cls.n)
        # define non-symmetric probability matrix as uneven
        cls.Pns = np.vstack(([0.6, 0.2], [0.3, 0.4]))
        # define symmetric probability as evenly weighted
        cls.Psy = np.vstack(([0.6, 0.2], [0.3, 0.4]))
        cls.Psy = symmetrize(cls.Psy)

    def test_binary_sbm(self):
        n = [50, 60, 70]
        vcount = np.cumsum(n)
        # define symmetric probability as evenly weighted
        Psy = np.vstack(([0.6, 0.2, 0.3], [0.3, 0.4, 0.2], [0.2, 0.8, 0.1]))
        Psy = symmetrize(Psy)
        np.random.seed(12345)
        A = binary_sbm(n, Psy)
        for i in range(0, len(n)):
            for j in range(0, len(n)):
                irange = np.arange(vcount[i] - n[i], vcount[i])
                jrange = np.arange(vcount[j] - n[j], vcount[j])

                block = A[(vcount[i] - n[i]):vcount[i],
                    (vcount[j] - n[j]):vcount[j]]
                if (i == j):
                    block = remove_diagonal(block)
                self.assertTrue(np.isclose(np.mean(block),
                    Psy[i, j], atol=0.02))
        self.assertTrue(is_symmetric(A))
        self.assertTrue(is_loopless(A))
        # check dimensions
        self.assertTrue(A.shape == (np.sum(n), np.sum(n)))
        pass

    def test_weighted_sbm_singlewt_undirected_loopless(self):
        np.random.seed(12345)
        wt = np.random.normal
        params = {'loc': 2, 'scale': 2}
        A = weighted_sbm(self.n, self.Psy, Wt=wt, Wtargs=params)
        for i in range(0, len(self.n)):
            for j in range(0, len(self.n)):
                irange = np.arange(self.vcount[i] - self.n[i], self.vcount[i])
                jrange = np.arange(self.vcount[j] - self.n[j], self.vcount[j])

                block = A[(self.vcount[i] - self.n[i]):self.vcount[i],
                    (self.vcount[j] - self.n[j]):self.vcount[j]]
                if (i == j):
                    block = remove_diagonal(block)
                self.assertTrue(np.isclose(np.mean(block != 0),
                    self.Psy[i, j], atol=0.02))
                self.assertTrue(np.isclose(np.mean(block[block != 0]),
                    params['loc'], atol=0.2))
                self.assertTrue(np.isclose(np.std(block[block != 0]),
                    params['scale'], atol=0.2))
        self.assertTrue(is_symmetric(A))
        self.assertTrue(is_loopless(A))
        # check dimensions
        self.assertTrue(A.shape == (np.sum(self.n), np.sum(self.n)))

    # below are the expectations of the estimators for the relevant weight
    # functions we exhaustively test
    def exp_normal(self, x):
        return({'loc': np.mean(x), 'scale': np.std(x)})

    def exp_poisson(self, x):
        return({'lam': np.mean(x)})

    def exp_exp(self, x):
        return({'scale': np.mean(x)})

    def exp_unif(self, x):
        return({'low': np.min(x), 'high': np.max(x)})

    def test_weighted_sbm_multiwt_directed_loopless(self):
        np.random.seed(12345)
        Wt = np.vstack(([np.random.normal, np.random.poisson],
            [np.random.exponential, np.random.uniform]))
        Wtargs = np.vstack(([{'loc': 2, 'scale': 2}, {'lam': 5}],
            [{'scale': 2}, {'low': 5, 'high': 10}]))
        check = np.vstack(([self.exp_normal, self.exp_poisson],
            [self.exp_exp, self.exp_unif]))
        A = weighted_sbm(self.n, self.Psy, Wt=Wt, directed=True, Wtargs=Wtargs)
        for i in range(0, len(self.n)):
            for j in range(0, len(self.n)):
                irange = np.arange(self.vcount[i] - self.n[i], self.vcount[i])
                jrange = np.arange(self.vcount[j] - self.n[j], self.vcount[j])

                block = A[(self.vcount[i] - self.n[i]):self.vcount[i],
                    (self.vcount[j] - self.n[j]):self.vcount[j]]
                if (i == j):
                    block = remove_diagonal(block)
                self.assertTrue(np.isclose(np.mean(block != 0),
                    self.Psy[i, j], atol=0.02))
                fit = check[i, j](block[block != 0])
                for k, v in fit.items():
                    self.assertTrue(np.isclose(v, Wtargs[i, j][k],
                        atol=0.2))
        self.assertFalse(is_symmetric(A))
        self.assertTrue(is_loopless(A))
        # check dimensions
        self.assertTrue(A.shape == (np.sum(self.n), np.sum(self.n)))
        pass

    def test_weighted_sbm_multiwt_undirected_loopless(self):
        np.random.seed(12345)
        Wt = np.vstack(([np.random.normal, np.random.poisson],
            [np.random.poisson, np.random.uniform]))
        Wtargs = np.vstack(([{'loc': 2, 'scale': 2}, {'lam': 5}],
            [{'lam': 5}, {'low': 5, 'high': 10}]))
        check = np.vstack(([self.exp_normal, self.exp_poisson],
            [self.exp_poisson, self.exp_unif]))
        A = weighted_sbm(self.n, self.Psy, Wt=Wt, directed=False, Wtargs=Wtargs)
        for i in range(0, len(self.n)):
            for j in range(0, len(self.n)):
                irange = np.arange(self.vcount[i] - self.n[i], self.vcount[i])
                jrange = np.arange(self.vcount[j] - self.n[j], self.vcount[j])

                block = A[(self.vcount[i] - self.n[i]):self.vcount[i],
                    (self.vcount[j] - self.n[j]):self.vcount[j]]
                if (i == j):
                    block = remove_diagonal(block)
                self.assertTrue(np.isclose(np.mean(block != 0),
                    self.Psy[i, j], atol=0.02))
                fit = check[i, j](block[block != 0])
                for k, v in fit.items():
                    self.assertTrue(np.isclose(v, Wtargs[i, j][k],
                        atol=0.2))
        self.assertTrue(is_symmetric(A))
        self.assertTrue(is_loopless(A))
        # check dimensions
        self.assertTrue(A.shape == (np.sum(self.n), np.sum(self.n)))
        pass

    def test_weighted_sbm_multiwt_directed_loopy(self):
        np.random.seed(12345)
        Wt = np.vstack(([np.random.normal, np.random.poisson],
            [np.random.exponential, np.random.uniform]))
        Wtargs = np.vstack(([{'loc': 2, 'scale': 2}, {'lam': 5}],
            [{'scale': 2}, {'low': 5, 'high': 10}]))
        check = np.vstack(([self.exp_normal, self.exp_poisson],
            [self.exp_exp, self.exp_unif]))
        A = weighted_sbm(self.n, self.Psy, Wt=Wt, directed=True, loops=True,
            Wtargs=Wtargs)
        for i in range(0, len(self.n)):
            for j in range(0, len(self.n)):
                irange = np.arange(self.vcount[i] - self.n[i], self.vcount[i])
                jrange = np.arange(self.vcount[j] - self.n[j], self.vcount[j])

                block = A[(self.vcount[i] - self.n[i]):self.vcount[i],
                    (self.vcount[j] - self.n[j]):self.vcount[j]]
                self.assertTrue(np.isclose(np.mean(block != 0),
                    self.Psy[i, j], atol=0.02))
                fit = check[i, j](block[block != 0])
                for k, v in fit.items():
                    self.assertTrue(np.isclose(v, Wtargs[i, j][k],
                        atol=0.2))
        self.assertFalse(is_symmetric(A))
        self.assertFalse(is_loopless(A))
        # check dimensions
        self.assertTrue(A.shape == (np.sum(self.n), np.sum(self.n)))
        pass

    def test_weighted_sbm_multiwt_undirected_loopy(self):
        np.random.seed(12345)
        Wt = np.vstack(([np.random.normal, np.random.poisson],
            [np.random.poisson, np.random.uniform]))
        Wtargs = np.vstack(([{'loc': 2, 'scale': 2}, {'lam': 5}],
            [{'lam': 5}, {'low': 5, 'high': 10}]))
        check = np.vstack(([self.exp_normal, self.exp_poisson],
            [self.exp_poisson, self.exp_unif]))
        A = weighted_sbm(self.n, self.Psy, Wt=Wt, directed=False, loops=True,
            Wtargs=Wtargs)
        for i in range(0, len(self.n)):
            for j in range(0, len(self.n)):
                irange = np.arange(self.vcount[i] - self.n[i], self.vcount[i])
                jrange = np.arange(self.vcount[j] - self.n[j], self.vcount[j])

                block = A[(self.vcount[i] - self.n[i]):self.vcount[i],
                    (self.vcount[j] - self.n[j]):self.vcount[j]]
                self.assertTrue(np.isclose(np.mean(block != 0),
                    self.Psy[i, j], atol=0.02))
                fit = check[i, j](block[block != 0])
                for k, v in fit.items():
                    self.assertTrue(np.isclose(v, Wtargs[i, j][k],
                        atol=0.2))
        self.assertTrue(is_symmetric(A))
        self.assertFalse(is_loopless(A))
        # check dimensions
        self.assertTrue(A.shape == (np.sum(self.n), np.sum(self.n)))
        pass