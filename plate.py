from cadquery import func as cf

plate = cf.box(80, 50, 10)          # length, width, height (mm)
hole = cf.cylinder(d=20, h=10)      # diameter, height
part = plate - hole                 # subtract = drill!

print(part.isValid(), round(part.Volume(), 1))
part.exportStl("plate.stl")
