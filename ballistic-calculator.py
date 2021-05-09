import matplotlib.pyplot as plt
from math import cos, sin
import csv

def dragCoefficient(v):

   # We use 341.5 m/s as our conversion from m/s to mach speed
   mach_conversion = 341.5

   # Open up the csv file holding the table of reference Cd values
   # IMPORTANT the file must be in the same location as this python script

   with open("G7DragFunction.csv") as G7DragFile:

       # We create a list containing the rows from the table
       G7Drag = list(csv.reader(G7DragFile))

       # Interpolation (v - v1) / (v2 - v1) = (Cdref - Cdref1) / (Cdref2 - Cdref1)
       # Cdref = (v - v1) / (v2 - v1) * (Cdref2 - Cdref1) + Cdref1

       # The bottom index will keep track of the last row the computer looked at
       bottom_index = 0

       # The computer will need to check the velocity for each row of the table, until we find the two rows (v1 and v2)
       # that are greater and less than v
       for row in G7Drag:

           # We use the float function to make sure that the computer recognizes the values in the table
           # as numbers and not text
           rowV = float(row[0]) * mach_conversion

           # If v is equal to the current row velocity, we can return the Cd value directly from the table
           if v - rowV == 0:
               return row[1]

           # If v is larger than the row velocity, we keep looking
           elif v - rowV > 0:
               bottom_index += 1

           # If v is less than the current row, we know v is in between v1 and v2
           elif v - rowV < 0:
               #At this point, the bottom_index is at the current row (which is v2) so we set the top index as the row for v2 and Cdref2
               top_index = bottom_index

            # If we want the values for v1 and Cdref1, we need to get the row one before the current row.
               v1 = float(G7Drag[bottom_index-1][0]) * mach_conversion
               Cdref1 = float(G7Drag[bottom_index - 1][1])

               # We then get the values for v2 and Cdref2
               v2 = float(G7Drag[top_index][0]) * mach_conversion
               Cdref2 = float(G7Drag[top_index][1])

               # Using our linear interpolation formula

               Cdref = (v - v1) / (v2 - v1) * (Cdref2 - Cdref1) + Cdref1
               return Cdref

# Constants
pi = 3.14
g = 9.81
tdelta = 0.001

# Inputs
airDensity = 1.203
BC = 0.2
muzzleVelocity = 900
muzzleAngle = 0.1
windVelocity = 5
windAngle = 45


BC = 703.7 * BC

muzzleAngle = muzzleAngle * pi / 180
windAngle = windAngle * pi / 180

xinitial = 0
vxinitial = muzzleVelocity * cos(muzzleAngle)

yinitial = 0
vyinitial = 0

zinitial = 0
vzinitial = muzzleVelocity * sin(muzzleAngle)

vtotal = muzzleVelocity

wx = windVelocity * -1 * cos(windAngle)
wy = windVelocity * -1 * sin(windAngle)

xList = []
vxList = []
axList = []

yList = []
vyList = []
ayList = []

zList = []
vzList = []
azList = []

for i in range(0,1000):

    Cdref = dragCoefficient(vtotal)

    ax = -0.125 * Cdref / BC * pi * airDensity * (vxinitial-wx)**2
    vxfinal = ax * tdelta + vxinitial
    xfinal = vxinitial * tdelta + xinitial

    ay = -0.125 * Cdref / BC * pi * airDensity * (vxinitial-wx) * (vyinitial-wy)
    vyfinal = ay * tdelta + vyinitial
    yfinal = vyinitial * tdelta + yinitial

    az = -0.125 * Cdref / BC * pi * airDensity * (vxinitial-wx) * vzinitial - g
    vzfinal = az * tdelta + vzinitial
    zfinal = vzinitial * tdelta + zinitial

    xList.append(xfinal)
    vxList.append(vxfinal)
    axList.append(ax)

    yList.append(yfinal)
    vyList.append(vyfinal)
    ayList.append(ay)

    zList.append(zfinal)
    vzList.append(vzfinal)
    azList.append(az)

    vtotal = (vxfinal**2 + vyfinal**2 + vzfinal**2)**0.5

    xinitial = xfinal
    vxinitial = vxfinal

    yinitial = yfinal
    vyinitial = vyfinal

    zinitial = zfinal
    vzinitial = vzfinal


trajectoryFig = plt.figure()
graph = trajectoryFig.add_subplot(411)
plt.ylabel("Z position")
plt.xlabel("X position")
plt.plot(xList, zList, 'b-')
plt.grid(True)

trajectoryFig.add_subplot(412, sharex=graph)
plt.ylabel("Y Position")
plt.xlabel("X position")
plt.plot(xList, yList, 'b-')
plt.grid(True)

plt.show()


