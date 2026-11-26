from dataclasses import dataclass
from cadquery import func as cf

@dataclass
class CellSpec:
    r_cell: float
    h_cell: float

def make_cell(spec):
    return cf.cylinder(d=2 * spec.r_cell, h=spec.h_cell)

# UPGRADED: Expanded width to host rows=2, and loop inside for Y offset positioning
def tray(spec, n=3, clearance=0.3, wall=4.0, thickness=6.0, depth=3.0, rows=2):
    pocket_r = spec.r_cell + clearance
    pitch = 2 * pocket_r + wall
    
    # UPGRADED: plate width supports 2 rows: (2 * pitch) + wall
    plate = cf.box(n * pitch + wall, rows * pitch + wall, thickness)
    
    pocket = cf.cylinder(d=2 * pocket_r, h=depth + 1).moved(z=thickness - depth)
    
    # UPGRADED: nested loops to generate a 2D grid of 2x3 pockets
    for r in range(rows):
        for i in range(n):
            x_offset = (i - (n - 1) / 2) * pitch
            y_offset = (r - (rows - 1) / 2) * pitch  # Centered perfectly around y=0
            plate = plate - pocket.moved(x=x_offset, y=y_offset)
            
    return plate

cells = {
    "18650": CellSpec(9.0, 65.0),
    "21700": CellSpec(10.5, 70.0),
    "4680": CellSpec(23.0, 80.0),
}

if __name__ == "__main__":
    for name, spec in cells.items():
        t = tray(spec)
        print(name, t.isValid(), round(t.Volume(), 1))
        t.exportStl(f"tray_{name}.stl")
