import cadquery as cq


class DotDict:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

def create_table(width, height, depth, initial_point, angle_x, angle_y, angle_z):
    # Create the top surface of the table
    table_top = cq.Workplane("XY").box(width, depth, height, centered=(True, True, True))

    # Rotate the table around x, y, and z axes
    rotated_table = table_top.rotate((0, 0, 0), (1, 0, 0), angle_x)
    rotated_table = rotated_table.rotate((0, 0, 0), (0, 1, 0), angle_y)
    rotated_table = rotated_table.rotate((0, 0, 0), (0, 0, 1), angle_z)

    # Find the position of the desired vertex after rotation
    # Assuming we want the lower front-left vertex
    vertex_after_rotation = rotated_table.val().Vertices()[1].toTuple()

    # Calculate the translation needed to move this vertex to the initial point
    translation_vector = (
        initial_point[0] - vertex_after_rotation[0],
        initial_point[1] - vertex_after_rotation[1],
        initial_point[2] - vertex_after_rotation[2]
    )

    # Translate the table to position the specified vertex at the initial point
    final_table = rotated_table.translate(translation_vector)

    return final_table


def slanted_board(width, base_height, top_height, cut_end, thickness, location, angle_x, angle_y, angle_z):
    # Define the 2D profile of the slanted figure with an intermediate point
    points = [
        (0, 0),  # Start at the base origin
        (0,top_height),
        (cut_end, top_height),
        (width, base_height),
        (width, 0),  # Back down to base level at width
    ]
    
    # Create the 2D profile
    profile = cq.Workplane("XY").polyline(points).close()
    
    # Extrude the 2D profile to the desired thickness
    solid = profile.extrude(thickness)

    # Rotate the solid to the desired orientation
    solid = solid.rotate((0, 0, 0), (1, 0, 0), angle_x)
    solid = solid.rotate((0, 0, 0), (0, 1, 0), angle_y)
    solid = solid.rotate((0, 0, 0), (0, 0, 1), angle_z)
    
    # Translate the solid to its final location
    solid = solid.translate(location) 
    return solid

def generate_general_console(parameters):
    p=DotDict(parameters)
    base_right_table = create_table(p.base_depth_g, p.base_height_g, p.general_board_thickness_g, (0, 0, 0), 0, 0, 0)
    base_left_table = create_table(p.base_depth_g, p.base_height_g, p.general_board_thickness_g, (0, p.organ_internal_width_g + p.general_board_thickness_g, 0), 0, 0, 0)
    base_back = create_table(p.organ_internal_width_g, p.base_height_g, p.general_board_thickness_g, (p.general_board_thickness_g, p.general_board_thickness_g, 0), 0, 0, 90)
    base_horizontal = create_table(p.organ_internal_width_g, p.top_depth_g, p.general_board_thickness_g, (0, p.general_board_thickness_g, p.base_height_g), 90, 0, 90)

    top_lateral_left = slanted_board(
        p.top_depth_g,  # width
        p.top_notch_start_y_g,   # base_height
        p.top_height_g,   # top_height
        p.top_notch_start_x_g,   # cut_start
        p.general_board_thickness_g,   # thickness
        (0, p.general_board_thickness_g, p.base_height_g),  # location
        90, 0, 0  # angles
    )

    top_lateral_right = slanted_board(
        p.top_depth_g,  # width
        p.top_notch_start_y_g,   # base_height
        p.top_height_g,   # top_height
        p.top_notch_start_x_g,   # cut_start
        p.general_board_thickness_g,   # thickness
        (0, p.organ_internal_width_g + p.general_board_thickness_g * 2, p.base_height_g),  # location
        90, 0, 0  # angles
    )

    top_back = create_table(p.organ_internal_width_g, p.top_height_g - 2 * p.general_board_thickness_g, p.general_board_thickness_g, (p.general_board_thickness_g, p.general_board_thickness_g, p.base_height_g + p.general_board_thickness_g), 0, 0, 90)
    top_front = create_table(p.organ_internal_width_g, p.top_height_g - 2 * p.general_board_thickness_g, p.general_board_thickness_g, (p.base_depth_g, p.general_board_thickness_g, p.base_height_g + p.general_board_thickness_g), 0, 0, 90)
    top_lid = create_table(p.organ_internal_width_g, p.base_depth_g, p.general_board_thickness_g, (0, p.general_board_thickness_g, p.base_height_g + p.top_height_g - p.general_board_thickness_g), 90, 0, 90)
    result = base_right_table + base_left_table + base_back + base_horizontal + top_lateral_left + top_lateral_right + top_back + top_front + top_lid

    return result