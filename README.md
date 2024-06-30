# Xray-codes
Xray data analysis codes


# XRD or Xray Diffraction


# XRR or Xray Reflectivity
for thin film

# GIXRD or Grazing Incidence XRD



# Installation 
1. Install Anaconda/conda 
2. Install pandas, matplotlib, scipy, sympy, jupyter

# Installation on Fedora (Using Terminal)
$ sudo dnf install conda

$ conda create -n xrd python=3.10

$ conda activate xrd

$ conda install pandas numpy matplotlib scipy seaborn jupyter sympy


# Explaining Algorithm behind miller-planes.py
1. Lattice parameters are a,b,c, alpha,beta,gamma
2. We've kept 'a' along 'x' axis and 'ab' plane in the 'xy' plane. It's just our convention.
3. We've found general expressions of eight corners of a unit cell.
4. The plot_surface method requires $X,Y,Z$ coordinates of four corners to plot the surface. Since there are no feature of the plane inside the boundary, $4$ corners are enough. Same thing is true for $3$ corner surfaces.


5. For a given $3-$component miller index, $(h,k,l)$, we scale the arm lengths by $a^\prime=a/f(h),\ b^\prime=b/f(k), c^\prime=c/f(l)$ and find coordinate of smaller cell. The function $f(x)$ returns absolute value of the argument is the argument is non zero else it returns 1.0.
6. In this way, $(h,k,l)$ for original unit cell will correspond to $(h^\prime,k^\prime,l^\prime)$ of the new cell and $h^\prime,k^\prime,l^\prime$ can only be one of $-1,0,+1$.


7. Now, to draw the plane we'll need to find the corners and the order of the corner that makes a loop. For example, ABCD rectangle will have AB, BC, CD, DA arms.
8. We predefine corner for $(100),(010),(001),(-100),(0-10),(00-1)$. If the miller index is $(101)$ then we take **unique** corners from all corners of $(100),(001)$. If the miller index is $(111)$ then we take **unique** corners from all corners of $(100),(001),(010)$. If the miller index is $(1-11)$ then we take **unique** corners from all corners of $(100),(001),(0-10)$. 
9. Now, we need to find the the order of those corners to make a loop. Few points (1) The dot product between adjacent arm can never be $0$ or $180$ degree (2) Arm length of opposite arm must be equal (3) Angle between opposite arm can be 


10. Now that we have the loop, we can find angles between planes by taking dot product of the normal vectors. To find the normal vector, we take two random and unique vectors on that plane and take cross product.


# Examples miller-planes.py
Assuming all packages are installed running the following command

$ python miller-planes.py

Creates the following plot
![Cubic Unit Cell](./res/plane%20(101).png)


The following command shows help in terminal 

$ python miller-planes.py -h