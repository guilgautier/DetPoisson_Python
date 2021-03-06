# Randomly simulates a determinantally-thinned Poisson point process. 
#
# A determinantally-thinned Poisson point process is essentially a discrete
# determinantal point process whose underlying state space is a single 
# realization of a Poisson point process defined on some bounded continuous 
# space. 
#
# For more details, see the paper by Blaszczyszyn and Keeler[1].
#
# Author: H.P. Keeler, Inria/ENS, Paris, and University of Melbourne, 
# Melbourne, 2018.
#
#References:
#[1] Blaszczyszyn and Keeler, Determinantal thinning of point processes with 
#network learning applications, 2018.

#import relevant libraries
import numpy as np
from scipy.linalg import orth
import scipy.stats
import matplotlib.pyplot as plt

#START -- Parameters -- START
#Poisson point process parameters
lambda0=50; #intensity (ie mean density) of the Poisson process

#choose kernel
choiceKernel=1;#1 for Gaussian (ie squared exponetial ); 2 for Cauchy
sigma=1;# parameter for Gaussian and Cauchy kernel
alpha=1;# parameter for Cauchy kernel

#Simulation window parameters
xMin=0;xMax=1;yMin=0;yMax=1;
xDelta=xMax-xMin;yDelta=yMax-yMin; #rectangle dimensions
areaTotal=xDelta*yDelta; #area of rectangle
#END -- Parameters -- END

#Simulate a Poisson point process
numbPoints = scipy.stats.poisson(lambda0*areaTotal).rvs();#Poisson number of points
xx = scipy.stats.uniform.rvs(0,xDelta,((numbPoints,1)))+xMin;#x coordinates of Poisson points
yy = scipy.stats.uniform.rvs(0,yDelta,((numbPoints,1)))+yMin;#y coordinates of Poisson points

# START -- CREATE L matrix -- START 
sizeL=numbPoints;
#Calculate Gaussian or kernel kernel based on grid x/y values
#all squared distances of x/y difference pairs
xxDiff=np.outer(xx, np.ones((numbPoints,)))-np.outer( np.ones((numbPoints,)),xx);
yyDiff=np.outer(yy, np.ones((numbPoints,)))-np.outer( np.ones((numbPoints,)),yy)
rrDiffSquared=(xxDiff**2+yyDiff**2);

if choiceKernel==1:
    #Gaussian/squared exponential kernel
    L=lambda0*np.exp(-(rrDiffSquared)/sigma**2);
    
elif choiceKernel==2:
        #Cauchy kernel
    L=lambda0/(1+rrDiffSquared/sigma**2)**(alpha+1/2); 
        
else:        
    raise Exception('choiceKernel has to be equal to 1 or 2.');
     
# END-- CREATE L matrix -- # END

# START Simulating/sampling DPP
#Eigen decomposition
eigenValuesL, eigenVectorsL=np.linalg.eig(L);
eigenValuesK = eigenValuesL / (1+eigenValuesL); #eigenvalues of K
indexEig = (np.random.rand(sizeL) < eigenValuesK );#Bernoulli trials

#number of points in the DPP realization
numbPointsDPP= np.sum(indexEig);  #number of points 
#retrieve eigenvectors corresponding to successful Bernoulli trials
spaceV = eigenVectorsL[:, indexEig]; #subspace V
indexDPP=list(); #list for index final DPP configuration

#Loop through for all points
for ii in range(numbPointsDPP):
    #Compute probabilities for each point i    
    Prob_i = np.sum(spaceV**2, axis=1);#sum across rows
    Prob_i = np.cumsum(Prob_i/ np.sum(Prob_i)); #normalize
    
    #Choose a new point using PMF Prob_i  
    indexCurrent=(np.random.rand() <= Prob_i).argmax();
    indexDPP.append(indexCurrent);    
    
    #Choose a vector to eliminate
    jj = (np.abs(spaceV[indexCurrent, :]) > 0).argmax() 
    columnVj = spaceV[:, jj];
    
    #Update matrix V by removing Vj component from the space
    spaceV = spaceV- (np.outer(columnVj,(spaceV[indexCurrent, :] / columnVj[indexCurrent]))); 
    #Orthonormalize (using singular value decomposition - could also use qr)
    spaceV = orth(spaceV);

#Loop finished   
indexDPP.sort(); #sort points
#END - Simulating/sampling DPP - END

#Plotting 
#Plot Poisson point process
plt.scatter(xx,yy, edgecolor='k', facecolor='none');
plt.xlabel("x"); plt.ylabel("y");
#random color vector
vectorColor=(np.asscalar(np.random.rand(1)), np.asscalar(np.random.rand(1)), np.asscalar(np.random.rand(1)));
#Plot determinantally-thinned Poisson point process
plt.scatter(xx[indexDPP],yy[indexDPP],edgecolor='none',facecolor=vectorColor);
