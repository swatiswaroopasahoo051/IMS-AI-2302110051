import math
from cadquery import func as cf

def clutch_brick(length, width, height, stud_d, stud_h, spacing, rows=2, cols=4):
    brick = cf.box(length, width, height)
    stud = cf.cylinder(d=stud_d, h=stud_h)
    
    for r in range(rows):
        for c in range(cols):
            x = (c - (cols - 1) / 2) * spacing
            y = (r - (rows - 1) / 2) * spacing
            brick = brick + stud.moved(x=x, y=y, z=height)
            
    return brick

# 2x4 brick dimensions: width = 15.6 mm (2 studs), length = 31.6 mm (4 studs)
brick = clutch_brick(31.6, 15.6, 9.6, 4.8, 1.7, 8.0, rows=2, cols=4)

# Updated expected volume for 8 studs
expected = 31.6 * 15.6 * 9.6 + 8 * math.pi * (4.8 / 2) ** 2 * 1.7
assert abs(brick.Volume() - expected) < 0.5

print("Valid:", brick.isValid(), "| Volume:", round(brick.Volume(), 2))
brick.exportStl("brick.stl")
