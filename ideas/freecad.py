import FreeCAD
import Part

def create_board_with_holes(width, height, thickness, rect_holes=[], circ_holes=[], min_height=0, min_width=0, rotation=(0, 0, 0), position=(0, 0, 0)):
    """Creates a board with holes, optional slant, rotation, and specific position."""

    # Create base shape (with or without slant)
    if min_height == 0 or min_width == 0:  # No slant
        board_shape = Part.makePolygon([FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(width, 0, 0), 
                                        FreeCAD.Vector(width, height, 0), FreeCAD.Vector(0, height, 0), 
                                        FreeCAD.Vector(0, 0, 0)])
    else:  # Slant
        board_shape = Part.makePolygon([FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(width, 0, 0),
                                        FreeCAD.Vector(width, height - min_height, 0),
                                        FreeCAD.Vector(min_width, height, 0),
                                        FreeCAD.Vector(0, height, 0),
                                        FreeCAD.Vector(0, 0, 0)])

    board = Part.Face(board_shape).extrude(FreeCAD.Vector(0, 0, thickness))

    # Create rectangular holes
    for x, y, hole_width, hole_height in rect_holes:
        if hole_width <= 0 or hole_height <= 0:
            FreeCAD.Console.PrintError(f"Invalid rect. hole dim.: w={hole_width}, h={hole_height}. Skipping.")
            continue
        if not (0 <= x <= width - hole_width and 0 <= y <= height - hole_height):
            FreeCAD.Console.PrintError("Rectangular hole outside boundaries. Skipping.")
            continue
        hole = Part.makeBox(hole_width, hole_height, thickness)
        hole.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, 0), FreeCAD.Rotation())
        board = board.cut(hole)

    # Create circular holes
    for x, y, radius in circ_holes:
        if radius <= 0:
            FreeCAD.Console.PrintError(f"Invalid circular hole radius: {radius}. Skipping.")
            continue
        if not (radius <= x <= width - radius and radius <= y <= height - radius):
            FreeCAD.Console.PrintError("Circular hole outside boundaries. Skipping.")
            continue
        hole = Part.makeCylinder(radius, thickness)
        hole.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, 0), FreeCAD.Rotation())
        board = board.cut(hole)

    # Apply rotation and position
    board.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(*rotation))
    board.Placement = FreeCAD.Placement(FreeCAD.Vector(*position), board.Placement.Rotation)

    if isinstance(board, Part.Compound):
        board = Part.makeSolid(board)

    return board


# Example usage:
width = 200
height = 100
thickness = 10
rect_holes = [(20, 20, 20, 20), (60, 30, 10, 40)]
circ_holes = [(120, 50, 15), (160, 20, 10)]
min_height = 20
min_width = 150
rotation = (0, 45, 0)
position = (100, 50, 20)

board_obj = create_board_with_holes(width, height, thickness, rect_holes, circ_holes, min_height, min_width, rotation, position)

if FreeCAD.ActiveDocument is None:
    FreeCAD.newDocument()

board_feature = FreeCAD.ActiveDocument.addObject("Part::Feature", "Board")
board_feature.Shape = board_obj

FreeCAD.ActiveDocument.recompute()