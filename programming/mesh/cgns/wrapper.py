import CGNS.MAP as cgm
import CGNS.PAT.cgnslib as cgl
import CGNS.PAT.cgnsutils as cgu
import CGNS.PAT.cgnskeywords as cgk
import sys
import numpy as np


def getChildrenByType(node, cgns_type):
    children = []
    all_children = cgu.getNextChildSortByType(node)
    for child in all_children:
        if cgu.checkNodeType(child, cgns_type):
            children.append(child)
    return children


def getChildrenByName(node, name):
    children = []
    all_children = cgu.getNextChildSortByType(node)
    for child in all_children:
        if getNodeName(child) == name:
            children.append(child)
    return children


def getUniqueChildByType(node, cgns_type):
    children = getChildrenByType(node, cgns_type)
    if 1 == len(children):
        return children[0]
    elif 0 == len(children):
        return None
    else:
        assert False


def getUniqueChildByName(node, name):
    children = getChildrenByName(node, name)
    if 1 == len(children):
        return children[0]
    elif 0 == len(children):
        return None
    else:
        assert False


def getNodeName(node) -> str:
    return node[0]


def getNodeData(node):
    return node[1]


def getNodeLabel(node) -> str:
    return node[-1]


def getDimensions(base) -> tuple[int, int]:
    assert 'CGNSBase_t' == getNodeLabel(base)
    return base[1][0], base[1][1]


def printInfo(file_name: str):
    cgns, _, _ = cgm.load(file_name)
    print(cgns)


def getUniqueZone(filename):
    tree, _, _ = cgm.load(filename)
    base = getUniqueChildByType(tree, 'CGNSBase_t')
    zone = getUniqueChildByType(base, 'Zone_t')
    zone_size = getNodeData(zone)
    assert zone_size.shape == (1, 3)
    return tree, zone, zone_size


def readPoints(zone, zone_size):
    n_node = zone_size[0][0]
    coords = getChildrenByType(
        getUniqueChildByType(zone, 'GridCoordinates_t'), 'DataArray_t')
    X, Y, Z = 0, 1, 2
    coords_x, coords_y, coords_z = coords[X][1], coords[Y][1], coords[Z][1]
    assert (n_node,) == coords_x.shape == coords_y.shape == coords_z.shape
    point_arr = np.ndarray((n_node, 3))
    for i in range(n_node):
        point_arr[i] = coords_x[i], coords_y[i], coords_z[i]
    return point_arr, coords_x, coords_y, coords_z


def removeSolutionsByLocation(zone, location):
    solutions = getChildrenByType(zone, 'FlowSolution_t')
    for solution in solutions:
        location_of_this_solution = getUniqueChildByType(solution, 'GridLocation_t')
        if location_of_this_solution is None:
            location_of_this_solution = 'Vertex'
        if location_of_this_solution == location:
            print(f'removing FlowSolution_t {solution} ...')
            cgu.removeChildByName(zone, getNodeName(solution))


if __name__ == '__main__':
    printInfo(sys.argv[1])
