import os
import argparse

def extract_nodes_between_tags(content):
    """
    Extracts lines between <Nodes> and </Nodes> tags from the given content.
    """
    nodes_start_index = content.index('<Nodes>\n') + 1
    nodes_end_index = content.index('</Nodes>\n')
    return content[nodes_start_index:nodes_end_index], content[nodes_end_index + 1:]

def main():

    # Create a parser
    parser = argparse.ArgumentParser(description="Command line options")

    # Add arguments
    parser.add_argument("--file",    type=str,  \
                        help="filename without extension", \
                        default = None)

    # Parse the arguments
    args  = parser.parse_args()

    # Read mesh file
    with open(args.file+'.mesh','r') as mesh_file:
        mesh_content = mesh_file.readlines()

    # Read mesh file
    with open(args.file+'.ipnodes','r') as ip_file:
        ipnodes_content = ip_file.readlines()

    # Extract nodes between <Nodes> and </Nodes> from polycrystal.ipnodes
    ipnodes_data, remaining_ipnodes_data = extract_nodes_between_tags(ipnodes_content)

    # Find the index of </Nodes> in polycrystal.mesh
    nodes_end_index = mesh_content.index('</Nodes>\n')

    # Insert the nodes from polycrystal.ipnodes before </Nodes> tag in polycrystal.mesh
    merged_content = mesh_content[:nodes_end_index] + ipnodes_data + mesh_content[nodes_end_index:]

    # Append any remaining data from polycrystal.ipnodes to the end of the merged content
    merged_content += remaining_ipnodes_data

    # Write the merged content back to a new file or overwrite the original polycrystal.mesh
    with open(args.file+'_merged.mesh', 'w') as merged_file:
        merged_file.writelines(merged_content)

    print("Merge completed!") 

if __name__ == "__main__":
    main()

