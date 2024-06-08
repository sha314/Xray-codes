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
        self.points_dict = {'O':OO, 'P':PP, 'Q':QQ, 'R':RR, 'S':SS, 'T':TT, 'U':UU, 'V':VV}
        self.points_label="OPQRSTUV"
        pass

    def get_planes(self, miller_index=(1,1,1)):
        """
        miller_index : as an array with 3 integer numbers, positive or negative

        100 or yz plane -> TUVS
        010 or zx plane -> RSVQ
        001 or xy plane -> PQVU
        """
        self.planes = {'100': 'TUVS', '010': 'RSVQ', '001': 'PQVU'}
        fullstr = ""
        if miller_index[0] > 0:
            fullstr += self.planes['100']
            pass
        if miller_index[1] > 0:
            fullstr += self.planes['010']
            pass
        if miller_index[2] > 0:
            fullstr += self.planes['001']
            pass
        countdict = {}
        for c in fullstr:
            if c in countdict.keys():
                countdict[c] += 1
                pass
            else:
                countdict[c] = 1
                pass
        finalstr = [c for c in countdict.keys() if countdict[c]==1 ]
        print(finalstr)
        return finalstr
        pass

    def draw(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        self.ax = ax
        
        self.draw_points()
        self.draw_unit_cell()
        # A,B,C,D = self.find_plane((1,0,0))
        OO, PP, QQ, RR, SS, TT, UU, VV = self.points
        # self.draw_plane_from_4_points(ax, PP, QQ, SS, TT, opacity=0.8)
        self.draw_plane_from_3_points(PP, TT, RR, opacity=0.8)
        self.find_normal_vector(UU, VV, SS, TT)
        self.find_normal_vector(OO, TT, SS, RR)
        self.find_normal_vector(PP, UU, VV, QQ)
        self.find_normal_vector(PP, TT, RR, RR)
        self.find_angle_between_planes((OO, PP, QQ, RR), (PP, RR, TT, PP))
        self.find_angle_between_planes((OO, PP, QQ, RR), (PP, QQ, SS, TT))
        self.find_angle_between_planes((OO, PP, QQ, RR), (PP, QQ, TT, SS))

        plt.legend()
        plt.show()
        pass


    def draw_points(self):
        ax = self.ax
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
        
    def draw_unit_cell(self):
        ax = self.ax
        OO, PP, QQ, RR, SS, TT, UU, VV = self.points

        # xy plane ORST -> arms OR, RS, ST, TO
        self.draw_plane_from_4_points(OO, RR, SS, TT)
        # xy plane PQVU
        self.draw_plane_from_4_points(PP, QQ, VV, UU)
        # yz plane, OPQR
        self.draw_plane_from_4_points(OO, PP, QQ, RR)
        # yz plane, TSVU
        self.draw_plane_from_4_points(TT, SS, VV, UU)
        # zx plane, OPUT
        self.draw_plane_from_4_points(OO, PP, UU, TT)
        # zx plane, RSVQ
        self.draw_plane_from_4_points(RR, SS, VV, QQ)

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

    def draw_plane_from_4_points(self, A, B, C, D, opacity=0.3):
        """
        ABCD rectangle. Four arms are AB, BC, CD, DA
        """
        ax = self.ax
        arr = np.array([[A, B],
                        [D, C]])
        X = arr[:,:,0]
        Y = arr[:,:,1]
        Z = arr[:,:,2]
        ax.plot_surface(X, Y, Z,  edgecolor='green', rstride=1, cstride=1, alpha=opacity)

        pass

    def draw_plane_from_3_points(self, A, B, C, opacity=0.3):
        """
        ABC Triangle. Three arms are AB, BC, CA
        """
        self.draw_plane_from_4_points(A, B, C, C, opacity)
        pass
    
    def find_angle_between_planes(self, plane1, plane2):
        A, B, C, D = plane1
        n1_hat = self.find_normal_vector(A, B, C, D)
        A, B, C, D = plane2
        n2_hat = self.find_normal_vector(A, B, C, D)
        angle = np.rad2deg(np.arccos(np.dot(n1_hat, n2_hat)))
        print("Angle between planes {:.3f} degree ".format(angle))
        pass

    def find_normal_vector(self, A, B, C, D):
        """
        vector normal of ABCD plane/rectangle.
        """
        # print("find_normal_vector")
        
        vec1 = np.array(A) - np.array(B)
        vec2 = np.array(C) - np.array(D)
        if np.dot(vec1, vec2) <= 1e-5:
            # If these are parallel vectors
            print("parallel")
            vec2 = np.array(A) - np.array(D)
            pass
        if np.dot(vec1, vec2) <= 1e-5:
            print("parallel")
            vec2 = np.array(A) - np.array(C)
            pass
        if np.dot(vec1, vec2) <= 1e-5:
            print("non-parallel vectors not found")
            exit(1)
            pass

        print("vec1 ", vec1)
        print("vec2 ", vec2)

        normal = np.cross(vec1, vec2)
        # print("normal ", normal)
        normal /= np.linalg.norm(normal)
        print("normal ", normal)
        return normal

    def find_loop(self, points):
        """
        3 or 4 points will be given, it will order them in a way that makes a loop.
          each step in the loop will represent an arm of the polygon.
        """
        AA, BB, CC, DD = points

        

        pass


cell1 = UnitCell(4,4,4,np.radians(90),np.radians(90),np.radians(90))
cell1.draw()
# cell1.find_plane((0,0,1))
cell1.get_planes((1,0,1))
cell1.get_planes((1,1,0))
cell1.get_planes((0,1,1))
cell1.get_planes((1,1,1))

cell1 = UnitCell(4,4,9,np.radians(90),np.radians(90),np.radians(120))
cell1.draw()

cell1 = UnitCell(4,9,4,np.radians(90),np.radians(120),np.radians(90))
cell1.draw()

cell1 = UnitCell(9,4,4,np.radians(120),np.radians(90),np.radians(90))
cell1.draw()

