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

parser.add_argument('-p', metavar='plot3D', type=int, nargs='+',
                    help='If 0 then an interactive 3D plot in matplotlib will be shown. If 1 then a heatmap.', default=[0])

parser.add_argument('-m', metavar='min_count', type=float, nargs='+',
                    help='Minimum counts in the scan', default=[10])

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
df = df.reindex(sorted(df.columns), axis=1)
# print(df)

df2 = pd.DataFrame()
psi_list.sort()
phi=np.arange(FirstAngle, ScanRange+StepWidth, StepWidth)
# print(phi.shape)
# print(len(psi_list))
zeros = [0]*(phi.shape[0]-len(psi_list))

## Writing to file
df2 = df.copy()
df2["psi"]=psi_list + zeros
df2["phi"]=phi
print("output file name ", path + "/" + args.o[0])
df2.to_csv(path + "/" + args.o[0])

## Display peaks in terminal
min_count = args.m[0]
df3 = df[df > min_count].fillna(0)
# print(df3)
# print(df3[12.0].values)
# print(df3[13.8].values)
df3 = df3.loc[:, (df3 != 0).any(axis=0)]
# print(df3)
# print(df3[12.6].values)
df3 = df3.loc[(df3 != 0).any(axis=1),:]
# print(df3)
phis = df2['phi'].iloc[df3.index.values]
# print(df3)
# df3 = df3.reindex(sorted(df3.columns), axis=1)
df3["phi"] = phis
print("Name of the columns represent psi angle")
print(df3)


# Plot 3D surface plot
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
print(df.shape)
if args.p[0] == 0:
    fig = plt.figure()
    
    ax = plt.axes(projection='3d')


    # Data for a three-dimensional line
    z = df.to_numpy().T
    x = phi
    y = np.array(psi_list)
    X, Y = np.meshgrid(x, y)
    # print(X[:,0])
    # print(X[:,1])

    # print(Y[:,0])
    # print(Y[:,1])
    # print(x.shape)
    # print(y.shape)
    # print(X.shape)
    # print(Y.shape)
    # print(z.shape)
    
    
    ax.plot_surface(Y, X, z, cmap='viridis', edgecolor='green', rstride=1, cstride=1)
    ax.set_xlabel('psi', fontsize=12)
    ax.set_ylabel('phi', fontsize=12)
    ax.set_zlabel('I(cps)', fontsize=12)
    plt.show()

    pass

elif args.p[0] == 1:

    fig, ax = plt.subplots()

    z = df.to_numpy().T
    x = phi
    y = np.array(psi_list)
    # X, Y = np.meshgrid(y, x)

    c = ax.pcolormesh(x, y, z, cmap='RdBu', vmin=min_count)
    ax.set_title('pole figure scan')
    # set the limits of the plot to the limits of the data
    # ax.axis([x.min(), x.max(), y.min(), y.max()])
    ax.set_ylabel('psi', fontsize=12)
    ax.set_xlabel('phi', fontsize=12)
    fig.colorbar(c, ax=ax)
    plt.show()

else:
    print("No plot arguments are provided")
    pass