# This code finds the psi angle of a bravis lattice with respect to it's orientaiton on the XRD Stage

import numpy as np
import pandas as pd
import glob
import argparse
import matplotlib.pyplot as plt





def draw_unit_cell_v2(a,b,c,alpha,beta,gamma):
    """
    yz plane (corners)-> OPQR
    xy plane          -> ORST
    zx plane          -> OPUT



    
    """

    OO = (0,0,0)
    TT = (a, 0, 0)
    SS = (a + b * np.cos(gamma), b*np.sin(gamma), 0)
    RR = (b*np.cos(gamma), b*np.sin(gamma), 0)
    PP = (c*np.cos(beta), c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
    QQ = (b*np.cos(gamma)+c*np.cos(beta), b*np.sin(gamma) + c*np.cos(alpha), c*np.sin(alpha))
    VV = (a + b*np.cos(gamma), b*np.sin(gamma) + c*np.cos(alpha), c*np.sin(beta))
    UU = (a + c*np.cos(beta), + c*np.cos(alpha), c*np.sin(beta))

    ax.scatter(OO[0],OO[1],OO[2], lw=4, label="O")
    ax.scatter(PP[0],PP[1],PP[2], lw=4, label="P")
    ax.scatter(QQ[0],QQ[1],QQ[2], lw=4, label="Q")
    ax.scatter(RR[0],RR[1],RR[2], lw=4, label="R")
    ax.scatter(SS[0],SS[1],SS[2], lw=4, label="S")
    ax.scatter(TT[0],TT[1],TT[2], lw=4, label="T")
    ax.scatter(UU[0],UU[1],UU[2], lw=4, label="U")
    ax.scatter(VV[0],VV[1],VV[2], lw=4, label="V")
    


    # xy plane ORST -> arms OR, RS, ST, TO
    
    arr = np.array([[OO, RR],
                  [TT, SS]])
    X = arr[:,:,0]
    Y = arr[:,:,1]
    Z = arr[:,:,2]
    ax.plot_surface(X, Y, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    # xy plane PQVU

    arr = np.array([[PP, QQ],
                  [UU, VV]])
    X = arr[:,:,0]
    Y = arr[:,:,1]
    Z = arr[:,:,2]
    ax.plot_surface(X, Y, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)


    # yz plane, OPQR
    arr = np.array([[OO, PP],
                  [RR, QQ]])
    X = arr[:,:,0]
    Y = arr[:,:,1]
    Z = arr[:,:,2]
    ax.plot_surface(X, Y, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)


    # yz plane, TSVU

    arr = np.array([[TT, SS],
                  [UU, VV]])
    X = arr[:,:,0]
    Y = arr[:,:,1]
    Z = arr[:,:,2]
    ax.plot_surface(X, Y, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)



    # zx plane, OPUT
    arr = np.array([[OO, PP],
                  [TT, UU]])
    X = arr[:,:,0]
    Y = arr[:,:,1]
    Z = arr[:,:,2]
    ax.plot_surface(X, Y, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    # zx plane, RSVQ
    arr = np.array([[RR, SS],
                  [QQ, VV]])
    X = arr[:,:,0]
    Y = arr[:,:,1]
    Z = arr[:,:,2]
    ax.plot_surface(X, Y, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_zlabel('z', fontsize=12)

    lim = [a,b,c]
    lim.sort()
    m=lim[-1]
    ax.set_xlim([0, m])
    ax.set_ylim([0, m])
    ax.set_zlim([0, m])

    
    pass


# We have lab coordinate (xyz) and crystal coordinate (abc)
def draw_unit_cell(a,b,c,alpha,beta,gamma):
    """
    ab plane of crystal sits on xy plane
    a,b,c : Lattice parameters
    alpha : angle between b and c
    beta  : angle between a and c
    gamma : angle between a and b
    """
    # xy(ab) plane
    coords = np.array([0,c])
    z = c * 1
    x = 2+np.array([0,b])
    y = np.array([0,a])*np.tan(gamma)


    X, Y = np.meshgrid(x, y)

    X = np.array([[0, a],
                  [b * np.cos(gamma), a + b*np.cos(gamma)]])
    
    Y = np.array([[0, 0],
                [b * np.sin(gamma), b*np.sin(gamma)]])


    Z = np.ones(X.shape)*z
    # Z = np.ones(X.shape)*z + np.array([[0, 0],[1, 1]])
    ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    z = c * 0
    Z = np.ones(X.shape)*z
    # Z = np.ones(X.shape)*z + np.array([[0, 0],[1, 1]])
    ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.3)





    X = np.array([[0, 0],
                  [b * np.cos(gamma), b*np.cos(gamma)]])
    
    Y = np.array([[0, 0],
                [b * np.sin(gamma), b * np.sin(gamma)]])
    
    Z = np.array([[0, c],
                [0, c]])


    ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)


    X = np.array([[a, a + b*np.cos(gamma)],
                  [a, a + b*np.cos(gamma)]])
    
    Y = np.array([[0, b * np.sin(gamma)],
                [0, b * np.sin(gamma)]])
    
    Z = np.array([[0, 0],
                [c, c]])


    ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)


    # z = c * 0
    # Z = np.ones(X.shape)*z
    # # Z = np.ones(X.shape)*z + np.array([[0, 0],[1, 1]])
    # ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.3)



    # # yz planes
    # z = coords
    # x = a * 1
    # y = coords
    # Y, Z = np.meshgrid(y, z)
    # X = np.ones(Y.shape)*x
    # ax.plot_surface(Y, X, Z, edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    # z = coords
    # x = a * 0
    # y = coords
    # Y, Z = np.meshgrid(y, z)
    # X = np.ones(Y.shape)*x
    # ax.plot_surface(Y, X, Z, edgecolor='green', rstride=1, cstride=1, alpha=0.3)

    # # zx planes
    # z = coords
    # x = coords
    # y = b * 1
    # X, Z = np.meshgrid(x, z)
    # Y = np.ones(X.shape)*y
    # ax.plot_surface(Y, X, Z, edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    # z = coords
    # x = coords
    # y = b * 0
    # X, Z = np.meshgrid(x, z)
    # Y = np.ones(X.shape)*y
    # ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.3)


    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_zlabel('z', fontsize=12)
    
    pass

    pass


def draw_unit_cube(cube_arm = 10):
    coords = np.linspace(0,cube_arm,5)
    # xy planes
    z = cube_arm * 1
    x = coords
    y = coords
    X, Y = np.meshgrid(x, y)
    Z = np.ones(X.shape)*z
    ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    z = cube_arm * 0
    x = coords
    y = coords
    X, Y = np.meshgrid(x, y)
    Z = np.ones(X.shape)*z
    ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.3)


    # yz planes
    z = coords
    x = cube_arm * 1
    y = coords
    Y, Z = np.meshgrid(y, z)
    X = np.ones(Y.shape)*x
    ax.plot_surface(Y, X, Z, edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    z = coords
    x = cube_arm * 0
    y = coords
    Y, Z = np.meshgrid(y, z)
    X = np.ones(Y.shape)*x
    ax.plot_surface(Y, X, Z, edgecolor='green', rstride=1, cstride=1, alpha=0.3)

    # zx planes
    z = coords
    x = coords
    y = cube_arm * 1
    X, Z = np.meshgrid(x, z)
    Y = np.ones(X.shape)*y
    ax.plot_surface(Y, X, Z, edgecolor='green', rstride=1, cstride=1, alpha=0.5)

    z = coords
    x = coords
    y = cube_arm * 0
    X, Z = np.meshgrid(x, z)
    Y = np.ones(X.shape)*y
    ax.plot_surface(Y, X, Z,  edgecolor='green', rstride=1, cstride=1, alpha=0.3)



    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_zlabel('z', fontsize=12)
    
    pass


# draw_unit_cube(7)


# draw_unit_cell(5,6,7,np.radians(90),np.radians(90),np.radians(45))
fig = plt.figure()
ax = plt.axes(projection='3d')
draw_unit_cell_v2(4,4,9,np.radians(90),np.radians(90),np.radians(120))
plt.legend()
plt.show()


fig = plt.figure()
ax = plt.axes(projection='3d')
draw_unit_cell_v2(4,9,4,np.radians(90),np.radians(120),np.radians(90))
plt.legend()
plt.show()
