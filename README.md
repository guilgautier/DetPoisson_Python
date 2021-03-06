# DetPoissonPython

Randomly simulates a determinantally-thinned Poisson point process on a rectangle.

A determinantally-thinned (Poisson) point process is essentially a discrete determinantal point process whose underlying state space is a single realization of a (Poisson) point process defined on some bounded continuous space. This is a repulsive point process, where the repulsion depends on the kernel and average density of points. For more details, see the paper by Blaszczyszyn and Keeler[1].

I wrote the simulation of the Poisson point process. To simulate the (discrete) determinantal point process, I modified the code in sample_dpp.py from this repository:

https://github.com/mbp28/determinantal-point-processes

I originally wrote all code in R and in MATLAB, which both have a very similar structure; see  

https://github.com/hpaulkeeler/DetPoisson_R 

https://github.com/hpaulkeeler/DetPoisson_MATLAB

It should be noted that there are a number of repositories with Python code that simulate (discrete) determinantal point process, including:

https://github.com/javiergonzalezh/dpp

https://github.com/mbp28/determinantal-point-processes

https://github.com/guilgautier/DPPy

https://github.com/ChengtaoLi/dpp

https://github.com/mehdidc/dpp

References: 

[1] Blaszczyszyn and Keeler, Determinantal thinning of point processes with network learning applications, 2018
.
