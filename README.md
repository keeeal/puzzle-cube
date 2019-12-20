# puzzle-cube

A randomly generated solid CAD puzzle cube. I wrote this as an exercise while learning how to generate 3D-printable objects using python.

![puzzle-cube](https://i.imgur.com/PfvlCmF.png)

## Usage

### Prerequisites

[SolidPython](https://github.com/SolidCode/SolidPython) and [Numpy](https://numpy.org/):

```
pip install solidpython numpy
```

### Running

```
python puzzle_cube.py [--size SIZE] [--shape X Y Z] [--sep] [--stl]
```

optional arguments:

 - *--size* — The size of a single cell of the puzzle. Default: 10 mm.
 - *--shape* — The dimensions of the puzzle. Default: (4, 4, 4)
 - *--sep* — Generate one file per puzzle piece. Otherwise all pieces will be generated in a single file.
 - *--stl* — Attempt to generate STL rather than SCAD files. This requires the OpenSCAD CLI to be available.
