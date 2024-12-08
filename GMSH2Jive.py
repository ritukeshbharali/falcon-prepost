# Python script to convert GMSH files to JIVE format

import sys
import gmsh
import os.path
import numpy as np
import argparse

from itemset     import ItemSet
from indexdict   import IndexDict
from node        import Node
from element     import Element

def parseGMSH( args ):

    fname    = args.file
    meshRank = args.meshRank

    # Create a element map for GMSH types
    # (elemID -> nnodes)
    elTypeToNNodes    = {}
    elTypeToNNodes[1] = 2   # Line2
    elTypeToNNodes[2] = 3   # Triangle3
    elTypeToNNodes[3] = 4   # Quad4
    elTypeToNNodes[8] = 3   # Line3
    elTypeToNNodes[9] = 6   # Triangle6

    # Initialize a database to store mesh data
    globdat            = {}
    globdat["nGroups"] = {}     # node groups
    globdat["eGroups"] = {}     # element groups

    # Create empty item sets to store nodes and elements
    nodeset    = ItemSet()
    elemset    = ItemSet()

    # Create an empty dictionary to store the element groups
    eGroups    = IndexDict()

    # All set, now initialize GMSH with no terminal output
    gmsh.initialize()
    gmsh.option.set_number('General.Terminal', 0)

    # Open the mesh file in gmsh (all versions should work!)
    gmsh.open(fname)

    # If .geo file is provided, generate and save the mesh
    ext    = os.path.splitext(fname)[1]
    ffname = os.path.splitext(fname)[0]

    if ext == ".geo":
        print(" -- Reading a mesh file: " + fname )
        try:
            gmsh.model.geo.synchronize()
            gmsh.model.mesh.generate(meshRank)
            gmsh.write(ffname +".msh")
            gmsh.open(ffname +".msh")
            print(" -- Created a mesh file: " 
              + ffname + ".msh")
        except Exception as e:
            raise e

    # Extract all nodes in the mesh
    nodes = gmsh.model.mesh.getNodes(dim=-1,tag=-1)

    # Add nodes to node set
    for i in range(len(nodes[0])):
        nodeset.addItem( idx=nodes[0][i],
                         item=Node(nodes[1][3*i:3*i+meshRank]) )

    # Get all entities associated with the gmsh model
    entities = gmsh.model.getEntities()

    # Sort entities such that higher 'dim' are ahead
    sorted_entities = sorted(entities, key=lambda x: (x[0], x[1]), reverse=True)

    # Element index
    elemIdx = 0

    # Loop over the entities
    for (dim,tag) in sorted_entities:

        # Extract physical groups, if present
        phyGroups = gmsh.model.getPhysicalGroupsForEntity(dim,\
                                                          tag)

        # Extract physical names, if phyGroups are found
        if phyGroups is []:
            phyNames  = []            
        else:
            try:
                phyNames  = gmsh.model.getPhysicalName(dim,\
                                                   phyGroups)
            except Exception as e:
                #print(e)
                phyNames  = gmsh.model.getPhysicalName(dim,\
                                                   phyGroups[0])
            

        # Extract elements for this entity
        elems = gmsh.model.mesh.getElements(dim=dim,tag=tag)

        # Extract number of nodes for the element type
        nNodes = elTypeToNNodes[elems[0][0]]

        # Add elements to elem set
        for i in range(len(elems[1][0])):
            elemIdx += 1
            elemset.addItem( idx=elemIdx,
                             item=Element(elems[2][0][nNodes*i:\
                                             nNodes*i+nNodes],
                                          gmshType=elems[0][0]) )
            
            # If there are physical names, create an element
            # group and add element indices to it
            if phyNames:
                eGroups.append( key=str(phyNames),
                                value=int(elemIdx) )
            # Otherwise, create an element group based on the tag
            # and add element indices to it
            else:
                eGroups.append( key="elemTag"+str(tag),
                                value=int(elemIdx) )

            eGroups.append( key="elems"+str(dim)+"D",
                                value=int(elemIdx) )

    # Store all info in globdat
    globdat["nSet"] = nodeset
    globdat["eSet"] = elemset

    globdat["eGroups"]        = eGroups
    globdat["eGroups"]['all'] = globdat["eSet"].getAllIndices()

    # Create special node groups
    for name, ielems in globdat["eGroups"].items():
        nodes = []
        for ielem in ielems:
            for inode in globdat["eSet"].getItem(ielem).getNodes():
                nodes.append(inode)
        nodes = np.unique(np.array(nodes,dtype=int))
        globdat["nGroups"][name] = nodes

    gmsh.finalize()

    print(" -- Parsed the mesh file: " + ffname + ".msh")
    print("    -- Nodes: " + str(nodeset.size()) )
    print("    -- Elems: " + str(elemset.size()) )
    print("       -- 1D: " + str(len(eGroups["elems1D"])) )
    print("       -- 2D: " + str(len(eGroups["elems2D"])) )
    if meshRank == 3:
        print("       -- 3D: " + str(len(eGroups["elems_3D"])) )

    return globdat

def printJiveMesh( args, globdat):

    fname = args.file

    # Create a element map for GMSH types
    # (elemID -> jive node ordering)
    elTypeToNodeOrd    = {}
    elTypeToNodeOrd[1] = np.array([0,1])           # Line2
    elTypeToNodeOrd[2] = np.array([0,1,2])         # Triangle3
    elTypeToNodeOrd[3] = np.array([0,1,2,3])       # Quad4
    elTypeToNodeOrd[8] = np.array([0,2,1])         # Line3
    elTypeToNodeOrd[9] = np.array([0,3,1,4,2,5])   # Triangle6

    ffname = os.path.splitext(fname)[0]

    with open(ffname+'.mesh', 'w') as fout:

        # Print nodes
        fout.write("<Nodes>\n")
        for i in sorted(globdat["nSet"].getAllIndices()):
            coords = globdat["nSet"].getItem(i).getCoords()
            fout.write(f"{i} {coords[0]} {coords[1]}; \n")
        fout.write("</Nodes>\n\n\n")

        # Print elements
        fout.write("<Elements>\n")
        for i in sorted(globdat["eSet"].getAllIndices()):
            enodes = globdat["eSet"].getItem(i).getNodes()
            perm   = elTypeToNodeOrd[globdat["eSet"].getItem(i).getGMSHType()]
            fout.write(f"{i} "+" ".join(map(str,enodes[perm]))+";\n") 
        fout.write("</Elements>\n\n\n")

        # Print node groups
        # Loop over all node groups
        for name, inodes in globdat["nGroups"].items():
            fout.write("<NodeGroup name="+ name +"Nodes>\n{")
            for inode in inodes:
                fout.write( str(inode) +",")
            fout.write("}\n</NodeGroup>\n\n")

        # Print node groups
        # Loop over all node groups
        for name, ielems in globdat["eGroups"].items():
            fout.write("<ElementGroup name="+ name +"Elems>\n{")
            for ielem in ielems:
                fout.write( str(ielem) +",")
            fout.write("}\n</ElementGroup>\n\n")

    return True

def printJiveIPNodes( args, globdat ):

    fname = args.file
    dim   = args.meshRank

    # Dummy IP nodes are printed only for domain elements
    # not face elements (one can change this construct!)

    # Create a element map for GMSH types
    # (elemID -> jive node ordering)
    elTypes    = {}
    elTypes[2] = np.array([2,3,9,10,16])
    elTypes[3] = np.array([4,5,6,7,11,12,13,14,17,18,19]) 

    nodeID = max(globdat["nSet"].getAllIndices())

    ipnodeset = ItemSet()
    ipGroups  = IndexDict()  # ip node groups

    # hard-coded for now!
    excluded_list = ["all","elems_1D","elems_2D","elems_3D"]

    # Loop over all element groups
    # (one IP node per element is assumed!) 
    for name, ielems in globdat["eGroups"].items():
        if name not in excluded_list:
            elType = globdat["eSet"].getItem(ielems[0]).getGMSHType()
            if dim == 2 and elType in elTypes[dim]:
                # Create dummy nodes
                for i in range(len(ielems)):
                    nodeID += 1
                    ipnodeset.addItem( idx=nodeID,
                                       item=Node( np.array([0.0, 0.0]) ) )
                    ipGroups.append( key=str(name),
                                       value=int(nodeID) )

    # Print them to a file
    if len(ipGroups) > 0:
        ffname = os.path.splitext(fname)[0]

        with open(ffname+'.ipnodes', 'w') as fout:

            # Print nodes
            fout.write("<Nodes>\n")
            for i in ipnodeset.getAllIndices():
                coords = ipnodeset.getItem(i).getCoords()
                fout.write(f"{int(i)} {coords[0]} {coords[1]}; \n")
            fout.write("</Nodes>\n\n\n")

            # Print node groups
            # Loop over all node groups
            for name, inodes in ipGroups.items():
                fout.write("<NodeGroup name="+ name +"IPNodes>\n{")
                for inode in inodes:
                    fout.write( str(inode) +",")
                fout.write("}\n</NodeGroup>\n\n")

    return True

def main():

    # Create a parser
    parser = argparse.ArgumentParser(description="Command line options")

    # Add arguments
    parser.add_argument("--file",    type=str,  \
                        help="filename with extension", \
                        default = None)
    parser.add_argument("--meshRank", type=int, \
                        help="mesh dimension (1,2,3)", \
                        default = 2)
    parser.add_argument("--sortElems",    type=bool, \
                        help="sort elements reverse dimension-wise", \
                        default = True)
    parser.add_argument("--ip", type=bool, \
                        help="print dummy IP nodes to file", \
                        default = False)

    # Parse the arguments
    args  = parser.parse_args()

    # Get filename and check for a valid extension
    fname  = args.file
    ext    = os.path.splitext(fname)[1]

    if ext != ".msh" and ext != ".geo":
        raise Exception("Illegal file format!" +
            "Only GMSH files with extension .msh or .geo are supported! ")

    # Parse GMSH mesh
    globdat = parseGMSH( args )

    # Print Jive mesh
    status  = printJiveMesh( args, globdat )

    # Check print status
    if status:
        print(" -- Printed Jive mesh file ")
    else:
        print(" -- GMSH to Jive mesh conversion: FAILED!")

    # Print Jive ip nodes
    if args.ip:
        status  = printJiveIPNodes( args, globdat )

        # Check print status
        if status:
            print(" -- Printed Dummy IP nodes to file ")
            print(" -- Use MergeDummyNodes.py to merge with the mesh file ")
        else:
            print(" -- Dummy IP nodes to file: FAILED!")


if __name__ == "__main__":
    main()