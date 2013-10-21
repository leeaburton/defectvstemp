#! /usr/bin/env python

###below contributed by ajjackson###
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",
                  action="store", type="string", dest="filename", default="geometry.in",
                  help="Path to input file [default: ./geometry.in]")
# Add further options here
(options, args) = parser.parse_args()

# Import columns 2:4 (python indexes from 0) from FHI-aims input file
lattice_vectors = np.genfromtxt(options.filename,skip_header=0, comments='#',usecols=(1,2,3))
# Truncate to top 3 rows
lattice_vectors = lattice_vectors[0:3,:]

# Get lattice vector magnitudes (a, b, c) according to Pythagoras' theorem
abc = np.sqrt(np.sum(np.square(lattice_vectors),1))

#volume is product of the three vector magnitudes
volume = np.prod(abc)

###below taken from ASE module###
fd = open(options.filename, 'r')
lines = fd.readlines()
fd.close()

symbols = []
for line in lines:
    inp = line.split()
    if inp == []:
        continue
    if inp[0] == 'atom' or inp[0] == 'atom_frac':
        symbols.append(inp[-1])

           
pickone = raw_input('Please specify the element symbol you wish me to calculate (case sensitive) ')  

sites = symbols.count(pickone)

#number of sites per angstrom cubed
perA = sites/ volume

#concentration per cm cubed
concn = perA*10**24

if sites == 0:
	print "No elements of that type"
else:
	print "There are", concn, pickone, "sites per cubic centimetre"

Ed = raw_input('Please input defect energy (eV) ')

Ed = float(Ed)

Kb = 8.6173324*10**-5 #eV K^-1

for T in range (1,1000):
	T = float(T)
	KbT = Kb*T
	arrhenius = concn*np.e**(-Ed/KbT)
	plt.plot(T,arrhenius,'ro')
plt.show()
