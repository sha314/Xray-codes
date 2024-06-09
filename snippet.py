
def find_plane(self, hkl=(1,0,0)):
        self.points_arr = np.array(self.points)
        print(self.points)
        print(self.points_arr)
        minx = np.min(self.points_arr[:,0])
        miny = np.min(self.points_arr[:,1])
        minz = np.min(self.points_arr[:,2])

        maxx = np.max(self.points_arr[:,0])
        maxy = np.max(self.points_arr[:,1])
        maxz = np.max(self.points_arr[:,2])

        mins = (minx, miny, minz)
        maxs = (maxx, maxy, maxz)

        print(mins)
        print(maxs)

        plane_coords = []
        xyz = 2
        collections = []
        if hkl[xyz] > 0: 
            
            max = 0
            for i in range(len(self.points)):
                a = self.points[i]
                print(self.points_label[i], " ", a)
                if (a[xyz] > max) and (abs(a[xyz]) > 1e-5):
                    # max = a[0]
                    plane_coords.append(self.points[i])
                    collections.append(self.points_label[i])
                    pass
                pass
            pass
        print(collections)
        print("plane_coords ", plane_coords)

        # self.draw_plane_from_4_points()
                

        return plane_coords