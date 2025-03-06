# Script to generate workflow settings JSON files for Albacore and Paramount systems
# Processes mapping data from Excel and creates formatted JSON configuration files
 
from statistics import mode
import pandas as pd
import json
from collections import OrderedDict

# Initialize variables
df_map = ''     # Will store the Excel data
albacore = False    # Flag for Albacore processing
paramount = False   # Flag for Paramount processing
albacoreMapDictionary = {}  # Store Albacore workflow mappings
queueMapDictionary = {}     # Store Paramount workflow mappings
queueWLDictionary = {}      # Store Paramount weblab mappings
albacoreOut = {}        # Final Albacore output structure
paramountOut = {}       # Final Paramount output structure

# Get user input for workflow type
flowType = input("Please choose mapping type (albacore/paramount):")
dictionary = "workflows"

# Load appropriate Excel sheet based on workflow type
if flowType == "albacore":
    df_map = pd.read_excel('map_data.xlsx', sheet_name="albacore")
    albacore = True
elif flowType == "paramount":
    df_map = pd.read_excel('map_data.xlsx', sheet_name="paramount")
    paramount = True

# Process Excel data row by row
for index, row in df_map.iterrows():
    if albacore:
        # Process Albacore mappings
        queue = row['queue']
        workflowId = row['albacore workflow id']
        if type(queue) != float and type(workflowId) != float:
            # Clean and format queue and workflow IDs
            queue = queue.replace('"', '')
            queue = queue.strip(" ")
            workflowId = workflowId.strip(',')
            workflowId = workflowId.strip(" ")
            workflowId = workflowId.replace('"', '')
            workflowId = workflowId.replace('[', '')
            workflowId = workflowId.replace(']', '')
            albacoreMapDictionary[queue] = [workflowId]
    elif paramount:
        # Process Paramount mappings
        queue = row['queue']
        workflowAndWebLab = row['workflow & weblab']
        if type(queue) != float and type(workflowAndWebLab) != float:
            # Clean and format queue and workflow/weblab data
            queue = queue.replace('"', '')
            queue = queue.strip(" ")
            workflowAndWebLab = workflowAndWebLab.strip(',')
            workflowAndWebLab = workflowAndWebLab.strip(" ")
            workflowAndWebLab = workflowAndWebLab.replace('"', '')
            workflowAndWebLab = workflowAndWebLab.replace('[', '')
            workflowAndWebLab = workflowAndWebLab.replace(']', '')
            # Separate weblabs from workflows
            if queue ==  "paramountWorkflowWeblabs":
                dictionary = "weblabs"
            if dictionary == 'weblabs':
                queueWLDictionary[queue] = [workflowAndWebLab]
            else:
                queueMapDictionary[queue] = [workflowAndWebLab]


# Generate output files based on workflow type
if albacore:
    # Create Albacore settings file
    albacoreMapDictionary = OrderedDict(sorted(albacoreMapDictionary.items()))
    albacoreOut["guidedWorkflowIds"] = albacoreMapDictionary
    albacoreOut = json.dumps(albacoreOut, indent=6)
    with open("guided-workflow-settings.json", "w") as mapfile:
        mapfile.write(albacoreOut)

    # Format and clean up JSON file
    # Remove extra whitespace and organize by marketplace
    with open(file='guided-workflow-settings.json', mode='r', encoding='UTF-8') as mapping_text:
        counter = 0
        new_text = ''
        for lines in mapping_text:
            if counter == 2:
                words = lines.split('_')
                marketplace = words[0].replace('"', '')  # AE
                marketplace = marketplace.replace(" ", '')
            if 0 <= counter < 2:
                new_text += lines
            elif ': [' in lines:
                lines = lines.replace('\n', '')
                new_text += lines
            elif '],' in lines:
                lines = lines.replace(" ", '')
                new_text += lines
            else:
                lines = lines.replace('\n', '')
                lines = lines.replace(" ", '')
                new_text += lines
            counter += 1

    # Write initial JSON
    with open("guided-workflow-settings.json", "w") as mapfile:
        mapfile.write(new_text)
    new_dictionary = ''
    counter = 0
    with open(file='guided-workflow-settings.json', mode='r', encoding='UTF-8') as mapfile:
        for lines in mapfile:
            # print(lines)
            old_marketplace = marketplace
            if counter > 1:
                words = lines.split('_')
                marketplace = words[0].replace('"', '')  # AU
                marketplace = marketplace.replace(" ", '')
            counter += 1
            if old_marketplace != marketplace:
                old_marketplace = marketplace
                new_dictionary += '\n' + lines
            else:
                new_dictionary += lines

    with open("guided-workflow-settings.json", "w") as mapfile:
        mapfile.write(new_dictionary)
else:
    # Create Paramount settings file
    queueMapDictionary = OrderedDict(sorted(queueMapDictionary.items()))
    queueWLDictionary = OrderedDict(sorted(queueWLDictionary.items()))
    paramountOut["paramountWorkflowIds"] = queueMapDictionary
    paramountOut["paramountWorkflowWeblabs"] = queueWLDictionary
    paramountOut = json.dumps(paramountOut, indent=6)
    # Write initial JSON
    with open("paramount-workflow-settings.json", "w") as mapfile:
        mapfile.write(paramountOut)

    # Format and clean up JSON file
    # Remove extra whitespace and organize by marketplace
    with open(file='paramount-workflow-settings.json', mode='r', encoding='UTF-8') as mapping_text:
        counter = 0
        new_text = ''
        for lines in mapping_text:
            if counter == 2:
                words = lines.split('_')
                marketplace = words[0].replace('"', '')  # AE
                marketplace = marketplace.replace(" ", '')
            if 0 <= counter < 2:
                new_text += lines
            elif ': [' in lines:
                lines = lines.replace('\n', '')
                new_text += lines
            elif '],' in lines:
                lines = lines.replace(" ", '')
                new_text += lines
            else:
                lines = lines.replace('\n', '')
                lines = lines.replace(" ", '')
                new_text += lines
            counter += 1

    with open("paramount-workflow-settings.json", "w") as mapfile:
        mapfile.write(new_text)
    new_dictionary = ''
    counter = 0

    with open(file='paramount-workflow-settings.json', mode='r', encoding='UTF-8') as mapfile:
        for lines in mapfile:
            # print(lines)
            old_marketplace = marketplace
            if counter > 1:
                words = lines.split('_')
                marketplace = words[0].replace('"', '')  # AU
                marketplace = marketplace.replace(" ", '')
            counter += 1
            if old_marketplace != marketplace:
                old_marketplace = marketplace
                new_dictionary += '\n' + lines
            else:
                new_dictionary += lines

    # Format cleanup process
    with open("paramount-workflow-settings.json", "w") as mapfile:
        mapfile.write(new_dictionary)

    print("done")


