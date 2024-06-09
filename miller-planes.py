# This code finds the psi angle of a bravis lattice with respect to it's orientaiton on the XRD Stage

import numpy as np
import pandas as pd
import glob
import argparse
import matplotlib.pyplot as plt


class UnitCell:
    """
    Unit Cell class
    Lattice parameters a,b,c,alpha,beta,gamma are provided and it can compute angles between planes and draw it.
    It also makes a 3D surface plot of the unit cell. Angles are in degree.

    Convention: arm 'a' is alsong 'x' axis and 'ab' plane is in 'xy' plane at z=0.
    Everything is computed based on this convention.
    
    """
    def __init__(self, a,b,c,alpha,beta,gamma) -> None:
        print("Creating new UnitCell object")
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta  = beta
        self.gamma = gamma
        OO, TT, SS, RR, PP, QQ, VV, UU = self.__calculate_points(a, b, c, alpha, beta, gamma)
        self.points = [OO, PP, QQ, RR, SS, TT, UU, VV]
        self.points_dict = {'O':OO, 'P':PP, 'Q':QQ, 'R':RR, 'S':SS, 'T':TT, 'U':UU, 'V':VV}
        self.points_label="OPQRSTUV"


        self.fig = plt.figure()
        ax = plt.axes(projection='3d')
        self.ax = ax
        pass

    def __calculate_points(self, a, b, c, alpha, beta, gamma):
        """
        Convention: arm 'a' is alsong 'x' axis and 'ab' plane is in 'xy' plane at z=0.
        Everything is computed based on this convention.
        """
        OO = (0,0,0.0)
        TT = (a, 0, 0.0)
        SS = (a + b * np.cos(gamma), b*np.sin(gamma), 0)
        RR = (b*np.cos(gamma), b*np.sin(gamma), 0)
        PP = (c*np.cos(beta), c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
        QQ = (b*np.cos(gamma)+c*np.cos(beta), b*np.sin(gamma) + c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
        VV = (a + b*np.cos(gamma) + c*np.cos(beta), b*np.sin(gamma) + c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
        UU = (a + c*np.cos(beta), + c*np.cos(alpha), c*np.sin(beta)* np.sin(alpha))
        # print("Original Points ", UU)
        return OO,TT,SS,RR,PP,QQ,VV,UU

    def get_scalled_points(self, miller):
        """
        If all 3 component of miller indices are 1 or 0 then this method doesn't do anything essentially.
        But if given miller index for a plane is (2,0,3) then we can compute coordinates of the corner of new
        unit cell by scaling the arm lengths of old (original) unit cell.
        a_new = a_old/2
        b_new = b_old  # cannot divide by zero
        c_new = c_old/3
        Then use the new arm lengths to compute the corner coordinates.
        Miller index (2,0,3) for original unit cell will correspond to (1,0,1) for new unit cell.
        """
        a, b, c = self.a, self.b, self.c
        alpha, beta, gamma = self.alpha, self.beta, self.gamma
        if miller[0] != 0:
            a /= miller[0]
            pass
        if miller[1] != 0:
            b /= miller[1]
            pass
        if miller[2] != 0:
            c /= miller[2]
            pass
        OO, TT, SS, RR, PP, QQ, VV, UU = self.__calculate_points(a, b, c, alpha, beta, gamma) 
        points_dict = {'O':np.array(OO), 'P':np.array(PP), 'Q':np.array(QQ), 'R':np.array(RR),
                             'S':np.array(SS), 'T':np.array(TT), 'U':np.array(UU), 'V':np.array(VV)}
        
        # print(self.points_dict)
        # print(points_dict)
        return points_dict
        pass

    def get_planes_from_miller_index(self, miller_index=(1,1,1)):
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
        if len(finalstr) == 3:
            # So that we always have 4 points for planes
            finalstr.append(finalstr[-1])
            pass
        print(finalstr)
        return finalstr
        pass

    
    def get_num_from_label_v3(self, label, miller):
        """
        with scalled corners
        """
        points_dict = self.get_scalled_points(miller)
        numbers = [points_dict[k] for k in label]
        return numbers

    def draw_plane_calculate_angle(self, miller1, miller2=(0,0,1)):
        """
        calculates angle between two planes.
        miller1 : arbitray plane with 3 component miller index. draws this plane
        miller2 : default is xy plane, with miller index (0,0,1). does not draw this plane
        """
        # self.draw_plane_calculate_angle_v2(miller1, miller2)

        corners1 = self.get_planes_from_miller_index(miller1)
        corners2 = self.get_planes_from_miller_index(miller2)
        # print("points1 ", corners1)
        # print("points2 ", corners2)
        self.find_angle_between_planes(miller1, miller2)
        points_dict = self.get_scalled_points(miller1)

        plane_found = False
        count = 0
        while not plane_found:
            count += 1
            AB = np.array(points_dict[corners1[1]]) - np.array(points_dict[corners1[0]])
            CD = np.array(points_dict[corners1[3]]) - np.array(points_dict[corners1[2]])
            if np.dot(AB, CD) <= 1e-5:
                # angle is more than 90 degrees
                # print("found order ", corners1)
                plane_found = True
            else:
                # rotate the elements in cyclic order
                # print("old order ", corners1)
                corners1 = corners1[:1] + corners1[1:]
                # print("new order ", corners1)
                pass
            if count >= 7:
                print("Cound not find correct order")
                break
            pass
        self.draw_plane_from_4_points(points_dict[corners1[1]], 
                                        points_dict[corners1[0]],
                                        points_dict[corners1[2]],
                                        points_dict[corners1[3]],
                                        opacity=0.8
                                        )
        pass


        pass
    def show(self):
        plt.legend()
        plt.show()
        pass
    
    def draw(self):
        """
        
        """
        self.draw_points()
        self.draw_unit_cell()

        #### Testing portion begin
        # A,B,C,D = self.find_plane((1,0,0))
        OO, PP, QQ, RR, SS, TT, UU, VV = self.points
        # self.draw_plane_from_4_points(ax, PP, QQ, SS, TT, opacity=0.8)
        # self.draw_plane_from_3_points(PP, TT, RR, opacity=0.8)
        # self.find_normal_vector(UU, VV, SS, TT)
        # self.find_normal_vector(OO, TT, SS, RR)
        # self.find_normal_vector(PP, UU, VV, QQ)
        # self.find_normal_vector(PP, TT, RR, RR)
        # self.find_angle_between_planes('OPQR','PRTP')
        # self.find_angle_between_planes('OPQR', 'PQST')
        # self.find_angle_between_planes('OPQR', 'PQTS')
        # self.find_angle_between_planes('PQVU', 'PQST')

        #### Testing portion end


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
    
    def find_normal_vector_v2(self, miller):
        """
        miller : miller index of the plane

        uses scalled corners
        
        It will find a string of four character, "ABCD"
        vector normal of ABCD plane/rectangle.

        If miller index is (201) then we can create a new unit cell wil sidex
        X_new = X_old/2
        and keep other sides the same.
        In this way (201) in old cell will correspond to (101) in new cell.
        """
        corners = self.get_planes_from_miller_index(miller)

        # print("find_normal_vector")
        A, B, C, D = self.get_num_from_label_v3(corners, miller)
        
        
        vec1 = np.array(A) - np.array(B)
        vec2 = np.array(C) - np.array(D)
        # print("vec1 ", vec1)
        # print("vec2 ", vec2)
        # print("cross ", np.cross(vec1, vec2))
        if np.linalg.norm(np.cross(vec1, vec2)) <= 1e-5:
            # If these are parallel vectors
            # print("parallel")
            vec2 = np.array(A) - np.array(C)
            pass
        
        # print("vec2 ", vec2)
        # print("cross ", np.cross(vec1, vec2))
        if np.linalg.norm(np.cross(vec1, vec2)) <= 1e-5:
            # print("parallel")
            vec2 = np.array(B) - np.array(C)
            pass
        
        # print("vec2 ", vec2)
        # print("cross ", np.cross(vec1, vec2))
        if np.linalg.norm(np.cross(vec1, vec2)) <= 1e-5:
            print("non-parallel vectors not found")
            exit(1)
            pass

        print("corners of plane ", corners)
        print("vec1 ", vec1)
        print("vec2 ", vec2)

        normal = np.cross(vec1, vec2)
        # print("normal ", normal)
        normal /= np.linalg.norm(normal)
        print("normal to the plane ", normal)
        return normal
    
    def find_angle_between_planes(self, miller1, miller2):
        """
        plane1 : labels of a plane corners
        plane2 : labels of a plane corners
        """
        n1_hat = self.find_normal_vector_v2(miller1)
        n2_hat = self.find_normal_vector_v2(miller2)
        angle = np.rad2deg(np.arccos(np.dot(n1_hat, n2_hat)))
        thestr = "Angle between planes {} and {} is {:.3f} degree ".format(miller1, miller2, angle)
        
        if angle > 90:
            thestr += " Or {:.3f} degree ".format(180-angle)
            pass
        print(thestr)
        
        pass


    def find_loop(self, points):
        """
        3 or 4 points will be given, it will order them in a way that makes a loop.
          each step in the loop will represent an arm of the polygon.
        """
        AA, BB, CC, DD = points

        

        pass


cell1 = UnitCell(4,4,4,np.radians(90),np.radians(90),np.radians(90))
# cell1.get_num_from_label_v2((0,0,2))
cell1.draw()
# cell1.draw_plane_calculate_angle((0,0,1))
# cell1.draw_plane_calculate_angle((1,1,1))
cell1.draw_plane_calculate_angle((2,0,1))
cell1.draw_plane_calculate_angle((0,1,1))
cell1.draw_plane_calculate_angle((1,1,0))

# cell1.find_normal_vector(['T', 'S', 'Q', 'P'])
# cell1.find_normal_vector("TSPQ")
# cell1.get_planes((1,0,1))
# cell1.get_planes((1,1,0))
# cell1.get_planes((0,1,1))
# cell1.get_planes((1,1,1))
cell1.show()

cell1 = UnitCell(4,4,9,np.radians(90),np.radians(90),np.radians(120))
cell1.draw()
# cell1.draw_plane_calculate_angle((1,1,1))
# cell1.draw_plane_calculate_angle((1,0,1))
# cell1.draw_plane_calculate_angle((1,0,2))
cell1.draw_plane_calculate_angle((2,0,1))
cell1.draw_plane_calculate_angle((0,1,1))
cell1.draw_plane_calculate_angle((1,1,0))
cell1.show()

cell1 = UnitCell(4,9,4,np.radians(90),np.radians(120),np.radians(90))
cell1.draw()
# cell1.draw_plane_calculate_angle((1,1,1))
# cell1.draw_plane_calculate_angle((1,0,1))
# cell1.draw_plane_calculate_angle((1,0,2))
# cell1.draw_plane_calculate_angle((0,1,1))
cell1.draw_plane_calculate_angle((1,1,0))
cell1.draw_plane_calculate_angle((2,0,1))
cell1.show()

cell1 = UnitCell(9,4,4,np.radians(120),np.radians(90),np.radians(90))
cell1.draw()
# cell1.draw_plane_calculate_angle((1,1,1))
# cell1.draw_plane_calculate_angle((1,0,1))
# cell1.draw_plane_calculate_angle((1,0,2))
# cell1.draw_plane_calculate_angle((0,1,1))
cell1.draw_plane_calculate_angle((1,1,0))
cell1.draw_plane_calculate_angle((2,0,1))
cell1.show()



