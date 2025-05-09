'''
This script adds the corresponding protein structures to the matching ligand pose files and save the complex as a new file. 
These ligand files were generated from docking results and then split into individual pose files using `split_compl.py`.

The combined files are prepared for molecular visualization.

At the beginning, the script prompts the user to provide paths to three folders:
- a folder containing the protein structure files,
- a folder with the ligand pose files,
- and a folder where the new combined files will be saved.

'''
import os

def merge_files(protein_folder, docking_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    protein_files = {f.split('.')[0]: f for f in os.listdir(protein_folder) if f.endswith('.pdbqt')}
    
    docking_files = [f for f in os.listdir(docking_folder) if f.endswith('.pdbqt')]

    for docking_file in docking_files:
        parts = docking_file.split('_')    # Protein name can be exstracted from docking result file 
        protein_name = parts[1]            # since it always has the same structer, for example: vina_6ick_MX3_out.pdbqt, 
                                           # where 6ick is the protein name.
        if protein_name in protein_files:    
            protein_file_path = os.path.join(protein_folder, protein_files[protein_name])
            docking_file_path = os.path.join(docking_folder, docking_file)
            output_file_path = os.path.join(output_folder, docking_file)

            with open(protein_file_path, 'r') as protein_file:
                protein_content = protein_file.readlines()

            with open(docking_file_path, 'r') as dock_file:
                dock_content = dock_file.readlines()

            insertion_index = 0                         # To insure that protein coordinates are added right befor the ligand pose, 
            for i, line in enumerate(dock_content):     # in case if smth is written befor the ligand pose.
                if line.startswith("MODEL"):
                    insertion_index = i
                    break

            merged_content = dock_content[:insertion_index] + protein_content + dock_content[insertion_index:]

            with open(output_file_path, 'w') as output_file:
                output_file.writelines(merged_content)
        else:
            print(f"Protein file for {protein_name} not found in {protein_folder}")

if __name__ == "__main__":
    protein_folder = input("Enter the name of the protein folder: ")
    docking_folder = input("Enter the name of the docking folder: ")
    output_folder = input("Enter the name of the output folder: ")

    merge_files(protein_folder, docking_folder, output_folder)