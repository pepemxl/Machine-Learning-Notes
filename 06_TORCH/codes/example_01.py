# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 11:14:59 2022

@author: pepem
"""


import torch
import numpy as np



def test_torch_01(array_sample:list):
    '''
    Testing creation of tensor with torch.

    Parameters
    ----------
    array_sample : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    t1 = torch.tensor(array_sample)
    print(t1)


def test_numpy_01(array_sample:list):
    '''
    Testing creation of tensors with numpy.

    Parameters
    ----------
    array_sample : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    t1 = np.array(array_sample)
    print(t1)

def test_torch_02():
    '''
    Testing creation of random tensor with torch.

    Returns
    -------
    None.

    '''
    t1 = torch.rand(2,2)
    print(t1)
    print(t1.shape)


def test_numpy_02():
    '''
    Testing creation of random tensor with numpy.

    Returns
    -------
    None.

    '''
    t1 = np.random.rand(2,2)
    print(t1)
    print(t1.shape)

def test_torch_03():
    '''
    Testing dot operator tensor with torch.

    Returns
    -------
    None.

    '''
    t1 = torch.rand(2,2)
    t2 = torch.rand(2,2)
    t3 = torch.matmul(t1,t2)
    print(t3.shape)
    print(t3)

def test_numpy_03():
    '''
    Testing dot operator tensor with numpy.

    Returns
    -------
    None.

    '''
    t1 = np.random.rand(2,2)
    t2 = np.random.rand(2,2)
    t3 = np.dot(t1,t2)
    print(t3.shape)
    print(t3)

def test_torch_04():
    '''
    Testing mult operator tensor with torch.

    Returns
    -------
    None.

    '''
    t1 = torch.rand(2,2)
    t2 = torch.rand(2,2)
    t3 = t1*t2
    print(t3.shape)
    print(t3)

def test_numpy_04():
    '''
    Testing mult operator tensor with numpy.

    Returns
    -------
    None.

    '''
    t1 = np.random.rand(2,2)
    t2 = np.random.rand(2,2)
    t3 = np.multiply(t1,t2)
    print(t3.shape)
    print(t3)

def run_test():
    print("\n\tTest tensor creation")
    array_sample = [[1,2,3],[4,5,6]]
    test_torch_01(array_sample)
    test_numpy_01(array_sample)
    print("\n\tTest random")
    test_torch_02()
    test_numpy_02()
    print('\n\tTest matrix operations')
    test_torch_03()
    test_numpy_03()
    test_torch_04()
    test_numpy_04()


if __name__ == '__main__':
    run_test()
    print(torch.eye(3))


