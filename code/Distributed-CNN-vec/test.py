#YOLO conv net
# import time
# from yolo import conv_forward,pool_forward
# from weights import image,W1,b1,W2,b2,W3,b3,hparameters1,hparameters2,hparameters3,hparameters4,hparameters5
# tic = time.process_time()
# out1=conv_forward(image, W1, b1, hparameters1) #3x3 s-1 pad-1 filters 16 activation-leaky
# out2=pool_forward(out1, hparameters2, mode = "max") #2x2 s-2
# out3=conv_forward(out2, W2, b2, hparameters3) #3x3 s-1 pad-1 filters 32 activation-leaky
# out4=pool_forward(out3, hparameters4, mode = "max") #2x2 s-2
# out5=conv_forward(out4, W3, b3, hparameters5) #3x3 s-1 pad-1 filters 32 activation-leaky
# toc = time.process_time()
# print ("Computation time = " + str(1000*(toc - tic)) + "ms")
# out5.shape

from offload import Offload
import pytest
import numpy as np
from vec import Pooling,vecConv
from yolo import pool_forward,conv_forward

def test_outshape():
    """
    X-numpy array numpy array (m,n_C, n_H, n_W)
    k-kernel (n_C, n_C_prev, f, f)
    out-(m,c,nh,nw)    
    """
    X = np.random.randn(10,4,5,7)
    W = np.random.randn(8,4,3,3)
    hparam = {"pad" : 1,
               "stride": 2}

    obj=Offload(1,1,1,X,W,hparam)
    assert obj.outShape() == (10,8,3,4)



def test_amountOfComputation():
    X = np.random.randn(1,1,4,4)
    W = np.random.randn(1,1,2,2)
    hparam = {"pad" : 0,
               "stride": 1}

    obj=Offload(1,1,1,X,W,hparam)
    assert obj.amountOfComputation()==9*7

def test_vecShape():
    X = np.random.randn(1,2,4,4)
    W = np.random.randn(1,2,2,2)
    hparam = {"pad" : 0,
               "stride": 1}

    obj=Offload(1,1,1,X,W,hparam)
    assert obj.vecShape()==(9,8)


def test_Pooling():
    np.random.seed(1)
    A_prev = np.random.randn(1, 5, 5, 3)
    hparameters = {"stride" : 1, "f": 2}
    max_output=pool_forward(A_prev, hparameters)
    np.testing.assert_array_equal(Pooling(A_prev[0,:,:,:],hparameters),max_output[0,:,:,:])

def test_conv():
    np.random.seed(1)
    A_prev = np.random.randn(1, 3, 3, 3)
    hparameters = {"pad" : 0,"stride": 1}
    w=np.ones((2,2,3,1))
    b=np.zeros(((1, 1, 1,1)))
    c_out=conv_forward(A_prev,w,b,hparameters)
    print(c_out.shape)
    print(c_out[0,:,:,:])
    v_out=vecConv(A_prev[0,:,:,:],w,hparameters)
    print(v_out.shape)
    print(v_out)
    np.testing.assert_array_equal(v_out,c_out[0,:,:,:])



