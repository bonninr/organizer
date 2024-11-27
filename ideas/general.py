from  organ_builder import create_board, DotDict
import cadquery as cq
from ocp_vscode import *

general_parameters = {
    "General_and_base": [
        {"organ_internal_width_g": 1300},
        {"general_board_thickness_g": 18},
        {"base_height_g": 800},
        {"base_depth_g": 350},
        {"base_front_distance_g": 10}
    ],
    "Volume_pedals": [
        {"volume_pedals_width_g": 12},
        {"volume_pedals_height_g": 24},
        {"volume_pedals_number_g": 2},
        {"volume_pedals_hole_start_height_g": 140}
    ],
    "Top": [
        {"top_depth_g": 650},
        {"top_height_g": 350},
        {"top_notch_start_x_g": 350},
        {"top_notch_start_y_g": 150}
    ]
}

def generate_general_console(parameters):
    p = DotDict(parameters)
    print (p)
    # Base right table
    base_right_table = create_board(
        max_width=p.base_depth_g,
        max_height=p.base_height_g,
        board_thickness=p.general_board_thickness_g,
        position=(0, 0, 0),
        rotation=(0, 0, 0)
    )

    # Base left table
    base_left_table = create_board(
        max_width=p.base_depth_g,
        max_height=p.base_height_g,
        board_thickness=p.general_board_thickness_g,
        position=(-p.organ_internal_width_g + p.general_board_thickness_g, 0, 0),
        rotation=(0, 0, 0)
    )

    # Base back
    base_back = create_board(
        max_width=p.organ_internal_width_g,
        max_height=p.base_height_g,
        board_thickness=p.general_board_thickness_g,
        position=(p.general_board_thickness_g, p.general_board_thickness_g, 0),
        rotation=(0, 0, 90)
    )

    base_front = create_board(
        max_width=p.organ_internal_width_g,
        max_height=p.base_height_g,
        board_thickness=p.general_board_thickness_g,
        position=(p.general_board_thickness_g, p.base_depth_g-100, 0),
        rotation=(0, 0, 90),
        rectangular_holes=[[p.organ_internal_width_g/2,300,300,300]]

    )

    # Base horizontal
    base_horizontal = create_board(
        max_width=p.organ_internal_width_g,
        max_height=p.top_depth_g,
        board_thickness=p.general_board_thickness_g,
        position=(0, p.general_board_thickness_g, p.base_height_g),
        rotation=(0, 90, 90)
    )

    # Top lateral left
    top_lateral_left = create_board(
        max_width=p.top_depth_g,
        max_height=p.top_height_g,
        min_width=p.top_notch_start_x_g,
        min_height=p.top_notch_start_y_g,
        board_thickness=p.general_board_thickness_g,
        position=(0, p.general_board_thickness_g, p.base_height_g),
        rotation=(00, 0, 0)
    )

    # Top lateral right
    top_lateral_right = create_board(
        max_width=p.top_depth_g,
        max_height=p.top_height_g,
        min_width=p.top_notch_start_x_g,
        min_height=p.top_notch_start_y_g,
        board_thickness=p.general_board_thickness_g,
        position=(-p.organ_internal_width_g + p.general_board_thickness_g * 2, 0, p.base_height_g),
        rotation=(00, 0, 00)
    )

    # Top back
    top_back = create_board(
        max_width=p.organ_internal_width_g,
        max_height=p.top_height_g - 2 * p.general_board_thickness_g,
        board_thickness=p.general_board_thickness_g,
        position=(p.general_board_thickness_g, p.general_board_thickness_g, p.base_height_g + p.general_board_thickness_g),
        rotation=(0, 0, 90)
    )

    # Top front
    top_front = create_board(
        max_width=p.organ_internal_width_g,
        max_height=p.top_height_g - 2 * p.general_board_thickness_g,
        board_thickness=p.general_board_thickness_g,
        position=(p.general_board_thickness_g, p.base_depth_g, p.base_height_g + p.general_board_thickness_g),
        rotation=(0, 0, 90)
    )

    # Top lid
    top_lid = create_board(
        max_width=p.organ_internal_width_g,
        max_height=p.base_depth_g,
        board_thickness=p.general_board_thickness_g,
        position=(0, p.general_board_thickness_g, p.base_height_g + p.top_height_g - p.general_board_thickness_g),
        rotation=(0, 90, 90)
    )

    result = base_right_table + base_left_table + base_back + base_front,  base_horizontal + \
             top_lateral_left + top_lateral_right + top_back + top_front + top_lid
    
    return result


show(generate_general_console(general_parameters))