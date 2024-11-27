import cadquery as cq
from ocp_vscode import *
import random
import string


class DotDict:
    def __init__(self, nested_dict):
        for category, items in nested_dict.items():
            # For each dictionary in the list
            for item_dict in items:
                # There should be only one key-value pair in each dictionary
                for key, value in item_dict.items():
                    # Add to flattened dictionary
                    setattr(self, key, value)

def create_board(max_width, max_height, board_thickness, position, rotation, min_width=0, min_height=0, rectangular_holes=[], circular_holes=[]):
    
    counter = str(random.randint(0, 100000))
    rot0=rotation[0]==90
    rot0, rot1, rot2 = rotation[0:3]
    if (rot1==90):
        rot0, rot1, rot2 = 90,-90,0 
    print ('const boardParams{} = {{maxWidth: {}, maxHeight:{},minWidth: {},minHeight: {}, boardThickness: {},position: {}, rotation: {}, rectangularHoles: [], circularHoles:[]}};'.format(counter, max_width/500, max_height/500, min_width/500, min_height/500, board_thickness/500, [position[1]/500, position[2]/500, position[0]/500], [rot0, rot2, rot1]))
    print ('scene.add(createBoard(boardParams{}, boxMaterial));'.format(counter))
    # Set the min height equal to max height if it's zero (for full rectangle)
    if min_height == 0:
        min_height = max_height

    # Create the points for the board shape
    points = [
        (0, 0),  # Lower left corner
        (max_width, 0),  # Lower right corner
        (max_width, min_height),  # Upper right corner
        (min_width, max_height),  # Transition for slanted edge
        (0, max_height)  # Upper left corner
    ]

    if min_width == 0:
        del points[3]  # Remove slanted edge if min_width is zero

    # Create the board by extruding the slanted rectangle shape
    board = cq.Workplane("YZ").polyline(points).close().extrude(board_thickness)

    # Calculate the offset from the center to the bottom-left corner
    x_offset = -max_width / 2
    y_offset = -max_height / 2

    # Add rectangular holes
    for hole in rectangular_holes:
        x, y, hole_width, hole_height = hole
        # Subtract half the width and height for bottom-left positioning
        hole_wp = board.faces(">X").workplane(centerOption="CenterOfBoundBox") \
            .transformed(offset=cq.Vector(x + x_offset, y + y_offset))
        board = hole_wp.rect(hole_width, hole_height).cutThruAll()

    # Add circular holes
    for hole in circular_holes:
        x, y, diameter = hole
        # Subtract half the width and height for bottom-left positioning
        hole_wp = board.faces(">X").workplane(centerOption="CenterOfBoundBox") \
            .transformed(offset=cq.Vector(x + x_offset, y + y_offset))
        board = hole_wp.circle(diameter / 2).cutThruAll()

    # Apply rotation and translation to position the board
    board = board.rotate((0, 0, 0), (1, 0, 0), rotation[0])
    board = board.rotate((0, 0, 0), (0, 1, 0), rotation[1])
    board = board.rotate((0, 0, 0), (0, 0, 1), rotation[2])

    board = board.translate(position)

    # Return the final CadQuery object
    return board


# Parameters for board creation
#max_width = 200
#max_height = 80
#board_thickness = 10
#position = (0, 0, 0)
#rotation = (0, 0, 0)
#min_width = 20
#min_height = 40

# Define holes (x, y, width, height for rectangular; x, y, diameter for circular)
#rect_holes = [(10, 10, 5, 10), (30, 30, 12, 15)]
#circular_holes = [(20, 20, 20), (40, 40, 20), (60, 60, 20)]

# Create and show the board with holes
#result = create_board(max_width, max_height, board_thickness, 
#                      position, rotation, min_width, min_height, 
#                      rect_holes, circular_holes)
#show(result)
