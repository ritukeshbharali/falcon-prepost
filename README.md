## falcon-preprost

falöcon-prepost is repository containing Python scripts to prepare input files for a Finite Element Analysis using [falcon](https://github.com/ritukeshbharali/falcon).

### Pre-requisites
- Python 3
- GMSH

### Usage

In the directory containing the .geo (say, problem.geo for a 2D mesh), execute:
```sh
python3 /path/to/GMSH2Jive.py --file problem.geo --meshRank 2
```

Additionally, one could pass Booleans to options *sortElems* and *ip*. *sortElems* renumbers the elements as 3D,2D,1D. *ip* creates dummy nodes for the integration points, which is special case. By default, *sortElems* and *ip* are set to False.

### Usage (special case)

If one needs dummy nodes for the integration points, in the directory containing .geo (say,  demo/polycrystal/polycrystal.geo), execute:

```sh
python3 /path/to/GMSH2Jive.py --file polycrystal.geo --meshRank 2 --sortElems True --ip True
```

This will create polycrystal.ipnodes. To include these nodes in the main mesh file polycrystal.mesh, execute:

```sh
python3 /path/to/MergeDummyNodes.py --file polycrystal
```

*Note that we pass the filename (polycrystal) without the extension here. This will merge contents of polycrystal.ipnodes and polycrystal.mesh to polycrystal_merged.mesh*

Additionally, one could pass Booleans to options *sortElems* and *ip*. *sortElems* renumbers the elements as 3D,2D,1D. *ip* creates dummy nodes for the integration points, which is special case. By default, *sortElems* and *ip* are set to False.

**Create an issue for feature requests and Pull Requests for bug fixes and other improvements.**