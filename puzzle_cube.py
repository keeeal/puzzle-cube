
from itertools import product
from subprocess import call
from os import remove

import numpy as np
from solid import *
from solid.utils import *

def save(obj, name, stl=False):
    scad_render_to_file(obj, name + '.scad')
    if stl:
        call(['openscad', name + '.scad', '-o', name + '.stl'])
        remove(name + '.scad')

def element(size, radius=1, tol=.2, segments=32):
    return hull()(tuple(translate([i,j,k])(sphere(radius, segments=32))
        for i, j, k in product(*3*[(radius + tol, size - radius - tol)])
    ))

def puzzle_cube(size=10.0, shape=(5,5,5), sep=False, stl=False):

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

    # get face shapes
    faces = []
    for n, (axis, end) in enumerate(product(range(3), (0, -1))):
        idx = 3*[slice(None)]
        idx[axis] = end
        faces.append(array[tuple(idx)] == n + 1)

    # save each piece as a separate file
    if sep:
        for n, face in enumerate(faces):
            piece = union()
            for i, row in enumerate(face):
                for j, value in enumerate(row):
                    if value:
                        piece += translate([size*i, size*j, 0])(element(size))
                        if i and face[i-1][j]:
                            piece += translate([size*(i-.5)+1, size*j+1, 1])(cube(size-2))
                        if j and face[i][j-1]:
                            piece += translate([size*i+1, size*(j-.5)+1, 1])(cube(size-2))

            save(piece, 'piece_' + str(n), stl=stl)

    # save all pieces as one file
    else:
        pieces = union()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=float, default=10.0)
    parser.add_argument('--shape', nargs=3, type=int, default=(5,5,5))
    parser.add_argument('--sep', action='store_true')
    parser.add_argument('--stl', action='store_true')
    puzzle_cube(**vars(parser.parse_args()))
