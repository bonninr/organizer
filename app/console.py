import cadquery as cq

organ_internal_width=1300
general_board_thickness=18
base_height=800
base_depth=350
base_front_distance=10

volume_pedals_width=12
volume_pedals_height=24
volume_pedals_number=2
volume_pedals_inbetween_separation=10
volume_pedals_lateral_separation=10
volume_pedals_hole_start_height=140
volume_pedals_hole_height=volume_pedals_height

top_depth=650
top_heigth=350
top_notch_start_x=350
top_notch_start_y=150

def assign_parameters(parameters):
  
    organ_internal_width=1300
    general_board_thickness=18
    base_height=800
    base_depth=350
    base_front_distance=10

    volume_pedals_width=12
    volume_pedals_height=24
    volume_pedals_number=2
    volume_pedals_inbetween_separation=10
    volume_pedals_lateral_separation=10
    volume_pedals_hole_start_height=140
    volume_pedals_hole_height=volume_pedals_height

    top_depth=650
    top_heigth=350
    top_notch_start_x=350
    top_notch_start_y=150  


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
        (0,top_heigth),
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

def generate_console():
    # Example usage



    music_sheet_board_width=750
    manual_side_boards=True

    base_right_table = create_table(base_depth, base_height, general_board_thickness, (0, 0, 0), 0, 0,0)

    base_left_table = create_table(base_depth, base_height, general_board_thickness, (0, organ_internal_width+general_board_thickness, 0), 0, 0,0)

    base_back = create_table(organ_internal_width, base_height, general_board_thickness, (general_board_thickness, general_board_thickness, 0), 0, 0,90)

    base_horizontal = create_table(organ_internal_width, top_depth, general_board_thickness, (0, general_board_thickness, base_height), 90, 0,90)

    top_lateral_left = slanted_board(
        top_depth,  # width
        top_notch_start_y,   # base_height
        top_heigth,   # top_height
        top_notch_start_x,   # cut_start
        general_board_thickness,   # thickness
        (0, general_board_thickness, base_height),  # location
        90, 0, 0  # angles
    )

    top_lateral_right = slanted_board(
        top_depth,  # width
        top_notch_start_y,   # base_height
        top_heigth,   # top_height
        top_notch_start_x,   # cut_start
        general_board_thickness,   # thickness
        (0, organ_internal_width+general_board_thickness*2, base_height),  # location
        90, 0, 0  # angles
    )


    top_back = create_table(organ_internal_width, top_heigth-2*general_board_thickness, general_board_thickness, (general_board_thickness, general_board_thickness, base_height+general_board_thickness), 0, 0,90)

    top_front = create_table(organ_internal_width, top_heigth-2*general_board_thickness, general_board_thickness, (base_depth, general_board_thickness, base_height+general_board_thickness), 0, 0,90)

    top_lid = create_table(organ_internal_width, base_depth, general_board_thickness, (0, general_board_thickness, base_height+top_heigth-general_board_thickness), 90, 0,90)

    result= base_right_table + base_left_table + base_back + base_horizontal + top_lateral_left + top_lateral_right + top_back + top_front + top_lid
    
    return result