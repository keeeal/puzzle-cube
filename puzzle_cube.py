
from itertools import product
from subprocess import call
from os import remove

import numpy as np
from solid import *
from solid.utils import *

def save(obj, name, stl=False, rm=True):
    scad_render_to_file(obj, name + '.scad')
    if stl:
        call(('openscad', name + '.scad', '-o', name + '.stl'))
        if rm: remove(name + '.scad')

def element(x, y, size, r=1, tol=.1, segments=32):
    return translate([size*x, size*y, 0])(hull()(
        tuple(translate([i, j, k])(sphere(r, segments=segments))
            for i, j, k in product(*3*[(r+tol, size-r-tol)]))))

def connector(x, y, size, r=1, tol=.1):
    return translate([size*x+r+tol, size*y+r+tol, r+tol])(cube(size-2*(r+tol)))

def puzzle_cube(size=10.0, shape=(5,5,5), stl=False, tol=.1):
    if any(i < 3 for i in shape):
        raise ValueError('Puzzle dimensions must be 3 or greater.')

    # make an array and number the faces
    x, y, z = shape
    face_values = (1, 2), (3, 4), (5, 6)
    array = np.pad(np.zeros((x - 2, y - 2, z - 2)), 1,
        constant_values=face_values)

    # randomly assign values along edges
    for axis in range(3):
        ends = 3*[(0, -1)]
        ends[axis] = (slice(None),)
        for idx in product(*ends):
            array[idx] = np.random.choice((
                face_values[axis - 1][idx[axis - 1]],
                face_values[axis - 2][idx[axis - 2]],
            ), shape[axis])

    # randomly assign values at corners
    for idx in product((0, -1), (0, -1), (0, -1)):
        delta = np.copysign(np.eye(3), idx).astype(np.int)
        array[idx] = np.random.choice(
            list(set(array[tuple(idx + i)] for i in delta)))

    # get faces
    faces = []
    for n, (axis, end) in enumerate(product(range(3), (0, -1))):
        idx = 3*[slice(None)]
        idx[axis] = end
        faces.append(array[tuple(idx)] == face_values[int(n/2)][n%2])

    # convert faces into solid pieces
    pieces = []
    for n, face in enumerate(faces):
        pieces.append(union())
        for i, row in enumerate(face):
            for j, value in enumerate(row):
                if value:
                    pieces[-1] += element(i, j, size, r=size/10, tol=tol)
                    if i and face[i-1][j]:
                        pieces[-1] += connector(i-.5, j, size, size/10, tol)
                    if j and face[i][j-1]:
                        pieces[-1] += connector(i, j-.5, size, size/10, tol)

    # save each piece as a separate file
    for n, piece in enumerate(pieces):
        save(piece, 'piece_' + str(n), stl=stl)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=float, default=10.0)
    parser.add_argument('--shape', nargs=3, type=int, metavar=('X','Y','Z'), default=(4,4,4))
    parser.add_argument('--stl', action='store_true')
    parser.add_argument('--tol', type=float, default=.1)
    puzzle_cube(**vars(parser.parse_args()))
