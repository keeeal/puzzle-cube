# puzzle-cube

A randomly generated solid CAD puzzle cube. I wrote this while learning how to generate 3D-printable objects using python.

![puzzle-cube](http://jameskeal.com.au/img/puzzle-cube-000.png)

## Usage

### Prerequisites

[SolidPython](https://github.com/SolidCode/SolidPython) and [Numpy](https://numpy.org/):

```
pip install solidpython numpy
```

### Running

```
python puzzle_cube.py [--size SIZE] [--shape X Y Z] [--stl]
```

optional arguments:

 - *--size* — The size-length of a single cell in the puzzle. Default: 10 mm.
 - *--shape* — The dimensions of the puzzle. Default: (4, 4, 4)
 - *--stl* — Attempt to generate STL rather than SCAD files. (Requires the OpenSCAD)
