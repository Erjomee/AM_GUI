import math


def get_xyz_of_points(xyz_point1: list, xyz_point2: list):
    """
    Get the x, y, z data of two points, combine them and return xs, ys and zs of both points
    :param xyz_point1: x, y, z coords of first point
    :param xyz_point2: x, y, z coords of second point
    :return: x_data, y_data, z_data
    """
    x_data = xyz_point1[0] + xyz_point2[0]
    y_data = xyz_point1[1] + xyz_point2[1]
    z_data = xyz_point1[2] + xyz_point2[2]
    return x_data, y_data, z_data


def calculate_distance(point1, point2):
    """
    Calculate the distance between two points in 3D space.

    Parameters:
    point1 (list): A list representing the coordinates (x, y, z) of the first point.
    point2 (list): A list representing the coordinates (x, y, z) of the second point.

    Returns:
    float: The distance between the two points.
    """

    # Calculate the differences in each coordinate
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dz = point2[2] - point1[2]

    # Calculate the distance using the Euclidean distance formula
    distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    return distance

