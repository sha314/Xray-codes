# This code can combine texture scan data exported to .xnn format

import numpy as np
import pandas as pd
import glob
import argparse



parser = argparse.ArgumentParser(
                    prog='TextureCombine',
                    description="Combines texture files. First column is the psi angle and 2nd column is phi angles, remaining columns are intenseties. Number of elements in psi column equals number of intensity columns.",
                    # epilog='Text at the bottom of help'
                    )


parser.add_argument('-d', metavar='folder', type=str, nargs='+',
                    help='Locationo of the folder containing .xnn files. Use double coute "" to ensure the name is passed properly')

parser.add_argument('-o', metavar='output filename', type=str, nargs='+',
                    help='name of the output file.', default="output.csv")

parser.add_argument('-p', metavar='plot3D', type=bool, nargs='+',
                    help='If true then an interactive 3D plot in matplotlib will be shown', default=True)

args = parser.parse_args()
print(args)
path=args.d[0]

print(path)
files=glob.glob(path+"/*.x00")

if len(files) == 0:
    print("No .xnn files in the specified directory or the directory does not exist")
    exit(1)
    pass

psi_list = []

df = pd.DataFrame()
for filename in files:
    with open(filename) as f:
        lines=f.readlines()
        # print(lines[:22])
        
        omega=float(lines[7].split()[-1])
        twoTheta=float(lines[8].split()[-1])
        psi=float(lines[12].split()[-1])
        psi_list.append(psi)
        FirstAngle = float(lines[15].split()[-1])
        ScanRange = float(lines[16].split()[-1])
        StepWidth = float(lines[17].split()[-1])
        TimePerStep = float(lines[18].split()[-1])
        NrOfData = float(lines[19].split()[-1])

        # print(psi)
        # print(omega)
        # print(twoTheta)
        # print(FirstAngle)
        # print(ScanRange)
        # print(StepWidth)
        # print(TimePerStep)
        # print(NrOfData)
        pass

    intensities=np.loadtxt(filename,skiprows=21)
    df[psi]=intensities
    pass


df2 = pd.DataFrame()
psi_list.sort()
phi=np.arange(FirstAngle, ScanRange+StepWidth, StepWidth)
# print(phi.shape)
# print(len(psi_list))
zeros = [0]*(phi.shape[0]-len(psi_list))
df2["psi"]=psi_list + zeros
df2["phi"]=phi

for psi in psi_list:
    # print(psi)
    df2[psi] = df[psi]
    pass

print("output file name ", path + "/" + args.o[0])
df2.to_csv(path + "/" + args.o[0])

# Plot 3D 
if args.p:
    from mpl_toolkits import mplot3d
    import numpy as np
    import matplotlib.pyplot as plt
    fig = plt.figure()
    
    ax = plt.axes(projection='3d')


    # Data for a three-dimensional line
    z = df.to_numpy()
    x = phi
    y = np.array(psi_list)
    X, Y = np.meshgrid(y, x)
    # print(x.shape)
    # print(y.shape)
    # print(z.shape)
    ax.plot_surface(X, Y, z, cmap='viridis', edgecolor='green')
    ax.set_xlabel('psi', fontsize=12)
    ax.set_ylabel('phi', fontsize=12)
    ax.set_zlabel('I(cps)', fontsize=12)
    plt.show()

    pass
