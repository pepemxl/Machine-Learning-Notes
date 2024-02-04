# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 19:29:46 2022

@author: pepem
"""
import torch
import numpy as np




def test_torch():
    data = [[1, 2],[3, 4]]
    x_data = torch.tensor(data)
    print(x_data)
    print(x_data.shape)
    
def test_torch_cuda():
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    cuda_device = torch.cuda.current_device()
    print(torch.cuda.get_device_name(cuda_device))

def test_memory_torch_cuda():
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')


if __name__=='__main__':
    test_torch_cuda()
    