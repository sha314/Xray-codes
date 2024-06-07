# This code finds the psi angle of a bravis lattice with respect to it's orientaiton on the XRD Stage

import numpy as np
import pandas as pd
import glob
import argparse
import matplotlib.pyplot as plt


class UnitCell:
    def __init__(self, a,b,c,alpha,beta,gamma) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta  = beta
        self.gamma = gamma
        self.__calculate_points()
        pass

    def __calculate_points(self):
        a, b, c = self.a, self.b, self.c
        alpha = self.alpha
        beta  = self.beta
        gamma = self.gamma

        OO = (0,0,0)
        TT = (a, 0, 0)
        SS = (a + b * np.cos(gamma), b*np.sin(gamma), 0)
        RR = (b*np.cos(gamma), b*np.sin(gamma), 0)
        PP = (c*np.cos(beta), c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
        QQ = (b*np.cos(gamma)+c*np.cos(beta), b*np.sin(gamma) + c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
        VV = (a + b*np.cos(gamma) + c*np.cos(beta), b*np.sin(gamma) + c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
        UU = (a + c*np.cos(beta), + c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))

        self.points = [OO, PP, QQ, RR, SS, TT, UU, VV]
        pass
    
    def draw(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        
        self.draw_points(ax)
        self.draw_unit_cell(ax)
        plt.legend()
        plt.show()
        pass


    def draw_points(self, ax):
        OO, PP, QQ, RR, SS, TT, UU, VV = self.points
        ax.scatter(OO[0],OO[1],OO[2], lw=4, label="O")
        ax.scatter(PP[0],PP[1],PP[2], lw=4, label="P")
        ax.scatter(QQ[0],QQ[1],QQ[2], lw=4, label="Q")
        ax.scatter(RR[0],RR[1],RR[2], lw=4, label="R")
        ax.scatter(SS[0],SS[1],SS[2], lw=4, label="S")
        ax.scatter(TT[0],TT[1],TT[2], lw=4, label="T")
        ax.scatter(UU[0],UU[1],UU[2], lw=4, label="U")
        ax.scatter(VV[0],VV[1],VV[2], lw=4, label="V")

        pass
        
    def draw_unit_cell(self, ax):
        OO, PP, QQ, RR, SS, TT, UU, VV = self.points

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

        lim = [self.a, self.b, self.c]
        lim.sort()
        m=lim[-1]
        ax.set_xlim([0, m])
        ax.set_ylim([0, m])
        ax.set_zlim([0, m])
        pass



cell1 = UnitCell(4,4,9,np.radians(90),np.radians(90),np.radians(120))
cell1.draw()

cell1 = UnitCell(4,9,4,np.radians(90),np.radians(120),np.radians(90))
cell1.draw()

cell1 = UnitCell(9,4,4,np.radians(120),np.radians(90),np.radians(90))
cell1.draw()

