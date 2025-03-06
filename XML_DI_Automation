# Script to create a Design Inspector output file from Paramount workflow BPMN code
# Reads from "paramount.xml" and creates "di_output.xml" for design-inspector.a2z.com

# Replace any " == " with " === " on the code without formatting the XML code

import random
import string

# Global variables initialization
random_id_list = [] # Stores generated random IDs to prevent duplicates
xml_string = ''     # Stores formatted XML content
step_name = ''      # Current step/section name
answer_object = ''  # Stores answer XML structure
section_object_id = ''  # Current section's ID
question_bank = {}  # Dictionary to store question ID-text pairs
answer_bank = {}    # Dictionary to store answer ID-text pairs
checkbox_list = []  # List to track checkbox questions

# Design Inspector XML variables for positioning and formatting
one_q_a_formation = ''  # Stores one question-answer pair XML
section_object = ''     # Stores section XML structure
question_object = ''    # Stores question XML structure
primary_canvas_id = 1   # Main canvas ID

# Position variables for questions and answers
q_x_position = 0
q_y_position = 0
a_x_position = 0
a_y_position = 0
section_x_pos = 0
section_y_pos = 0
height_box = 0
xml_code = ''

# Initial XML structure for Design Inspector
initial_xml_code = f'<?xml version="1.0" encoding="UTF-8"?><mxGraphModel dx="861" dy="574" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0"><root><mxCell id="0" nextCellIdValue="8"><ResourceDescriptor resource="_:0" serialization-version="v0" as="resourceDescriptor"><SemanticDataContainer serialization-version="v0"><StringLiteral content="0" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/a2255956-c3df-4c2c-b489-c307f68abc97" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/84a80b5f-5642-4a17-9585-ebfdb65f4bec" property="https://ontology.security.amazon.dev/foundation/system-modeling/04539597-4283-4f65-8090-ae67f9d3e949" /></SemanticDataContainer></ResourceDescriptor></mxCell><mxCell id="{primary_canvas_id}" parent="0"><ResourceDescriptor resource="_:{primary_canvas_id}" serialization-version="v0" as="resourceDescriptor"><SemanticDataContainer serialization-version="v0"><StringLiteral content="1" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/a2255956-c3df-4c2c-b489-c307f68abc97" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/84a80b5f-5642-4a17-9585-ebfdb65f4bec" property="https://ontology.security.amazon.dev/foundation/system-modeling/04539597-4283-4f65-8090-ae67f9d3e949" /></SemanticDataContainer></ResourceDescriptor></mxCell>'


def readingXMLFile():
    """
    Reads and formats the BPMN XML file
    - Adds line breaks after '>' for better readability
    - Saves formatted XML back to file
    - Initiates data extraction process
    """
    global xml_string
    line = ''
    # Formatting the XML Code for better code alignment
    with open(file='paramount.xml', encoding='UTF-8', mode='r') as xml_file:
        for lines in xml_file:
            for words in lines:
                if words != '>':
                    line += words
                if words == '>':
                    line = line + '>'
                    xml_string += line + '\n'
                    line = ''
        xml_file.close()

    with open(file='paramount.xml', encoding='UTF-8', mode='w') as f:
        f.write(xml_string)
        f.close()
    # XML code formatted and saved in the same .txt file

    extractingData()


def question_collector():
    """
    Collects all questions and answers from the BPMN file
    - Populates question_bank and answer_bank dictionaries
    - Handles different question types (SELECT, YES/NO, STRING, etc.)
    """
    global question_bank, answer_bank
    try:
        with open(file='paramount.xml', encoding='UTF-8', mode='r') as xml_file:
            for lines in xml_file:
                if 'CDATA[' in lines:
                    continue
                if r'"supplementalInfo\"' not in lines:
                    if 'SELECT_BUTTON' in lines or 'SELECT_RADIO' in lines:
                        lines = lines.split('"')
                        question = lines[3].rstrip('\\')
                        question = question.replace('&#34;', '')
                        question = question.replace('&#39;', '')
                        question_id = lines[1].rstrip('\\')
                        question_bank[question_id] = question
                    if 'YES_NO_QUESTION' in lines:
                        lines = lines.split('"')
                        question = lines[3].rstrip('\\')
                        question = question.replace('&#34;', '')
                        question = question.replace('&#39;', '')
                        question_id = lines[1].rstrip('\\')
                        question_bank[question_id] = question
                    if r'"STRING\"' in lines:
                        lines = lines.split('"')
                        question = lines[3].rstrip('\\')
                        question = question.replace('&#34;', '')
                        question = question.replace('&#39;', '')
                        question_id = lines[1].rstrip('\\')
                        question_bank[question_id] = question
                    if 'SELECT_ONE' in lines:
                        lines = lines.split('"')
                        question = lines[3].rstrip('\\')
                        question = question.replace('&#34;', '')
                        question = question.replace('&#39;', '')
                        question_id = lines[1].rstrip('\\')
                        question_bank[question_id] = question
                    if 'CHECKBOX' in lines:
                        lines = lines.split('"')
                        question = lines[3].rstrip('\\')
                        question = question.replace('&#34;', '')
                        question = question.replace('&#39;', '')
                        question_id = lines[1].rstrip('\\')
                        question_bank[question_id] = question
                    if r'options.' in lines:
                        lines = lines.split('"')
                        answers = lines[1].split('.')
                        print(answers)
                        answer_value = answers[1]
                        answer_id = lines[3].rstrip('\\')
                        answer_bank[answer_id] = answer_value
    except Exception as error_found:
        print(f"Error_found in line : {lines} ; Exception : {error_found}")
        

def tooltip_generator(line):
    """
    Generates tooltip text for questions with conditional logic
    Args:
        line: XML line containing conditional expression
    Returns:
        Formatted tooltip string showing question-answer relationships
    """
    global question_bank, answer_bank
    pre_answer = '&lt;div&gt;'
    post_answer = '&lt;/div&gt;'
    lines = line
    tooltip = ''
    # print(lines)
    fup_question = lines[3].split('||')
    fup_q_a_list = []
    not_equal = False
    try:
        if len(fup_question) > 1:
            for items in fup_question:
                q = ''
                q_a_item = items.split('===')
                questions = q_a_item[0]
                answers = q_a_item[1]
                answer = answers.replace('&#39;', '')
                answer = answer.replace('&#34;', '')
                answer = answer.replace(')', '')
                answer = str(answer.strip(' ').replace('\\', ''))
                answer_check = answer.lower()
                questions = questions.replace('eval', '')
                questions = questions.replace('(', '')
                questions = questions.replace(')', '')
                questions = questions.replace(' ', '')
                questions = questions.replace(' ', '')
                if answer_check == "true" or answer_check == "false" or answer_check == "True" or answer_check == "False":
                    q_length = len(questions)
                    i = 0
                    for chars in questions:
                        if i < q_length / 2:
                            q += chars
                            i += 1
                    questions = q
                    if answer_check == "True" or answer_check == "true":
                        answer_bank[answer_check] = "Yes"
                    elif answer_check == "False" or answer_check == "false":
                        answer_bank[answer_check] = "No"
                fup_q_a_list.append(questions)
                # print(answer)
                fup_q_a_list.append(answer)
            i = 0
            for items in fup_q_a_list:
                # question_bank (Collection of question ids and label)
                # answer_bank (Collection of answer ids and label)
                if i % 2 == 0:
                    value = question_bank[items]
                    tooltip += pre_answer + str(value) + " : "
                else:
                    value = answer_bank[items]
                    tooltip += str(value) + post_answer
                i += 1
            fup_q_a_list.clear()
        else:
            q_a_item = lines[3]
            if('===' in q_a_item):
                q_a_item = q_a_item.split('===')
            elif('!=' in q_a_item):
                q_a_item = q_a_item.split('!=')
                value = "!="
                not_equal = True
            question = q_a_item[0]
            questions = question.replace('eval(', '')
            questions = questions.replace(')', '')
            questions = questions.replace(' ', '')
            print(q_a_item)
            answer = q_a_item[1]
            answer = answer.replace('&#39;', '')
            answer = answer.replace('&#34;', '')
            answer = answer.replace(')', '')
            answer = str(answer.strip(' ').replace('\\', ''))
            answer_check = answer.lower()
            q = ''
            if answer_check == "true" or answer_check == "false" or answer_check == "True" or answer_check == "False":
                q_length = len(questions)
                i = 0
                for chars in questions:
                    if i < q_length / 2:
                        q += chars
                        i += 1
                questions = q
                if answer_check == "True" or answer_check == "true":
                    answer_bank["True"] = "Yes"
                    answer_bank["true"] = "Yes"
                elif answer_check == "False" or answer_check == "false":
                    answer_bank["False"] = "No"
                    answer_bank["false"] = "No"
            fup_q_a_list.append(questions)
            fup_q_a_list.append(answer)
            # fup_q_a_list.append(questions)
            # fup_q_a_list.append(answer)
            i = 0
            for items in fup_q_a_list:
                # question_bank (Collection of question ids and label)
                # answer_bank (Collection of answer ids and label)
                if i % 2 == 0:
                    value = question_bank[items]
                    if not_equal:
                        tooltip += pre_answer + str(value) + " != "
                        not_equal = False
                    else:
                        tooltip += pre_answer + str(value) + " : "
                else:
                    value = answer_bank[items]
                    tooltip += str(value) + post_answer
                i += 1
            fup_q_a_list.clear()
    except Exception as exp:
        print(exp, " : ", questions, " || answers : ", answer)
    return tooltip


def extractingData():
    """
    Main function to process BPMN XML and create Design Inspector structure
    - Processes different question types
    - Manages section creation and positioning
    - Handles question-answer relationships
    - Creates visual representation structure
    """
    global xml_string, step_name, one_q_a_formation, xml_code, question_bank, answer_bank, a_y_position, height_box
    q_a_call_counter = 0
    section_call_counter = 0
    found_select_one_button = False
    found_select_radio_button = False
    found_string_question = False
    yes_no_question_found = False
    answer_dictionary = {}
    a_number = 0
    new_section_found = False
    found_checkbox = False
    tooltip = ''
    counter_reset = False
    checkbox_count = 0
    checkbox_indicator = False
    question_collector()
    with open(file='paramount.xml', encoding='UTF-8', mode='r') as xml_file:
        for lines in xml_file:
            if '<bpmn:scriptTask id=' in lines or '<![CDATA[' in lines:
                continue
            lines = str(lines)
            if '<bpmn:userTask id=' in lines:
                question_counter = 0
                found_initial = True
                # Capturing the task name

                lines = lines.split('"')
                section_list = lines[3].split(' ')
                if '&#10;_VIP' in lines[3]:
                    section_list = lines[3].rstrip('&#10;_VIP\\')
                elif '&#10;' in lines[3]:
                    section_list = lines[3].replace('&#10;', '')
                    section_list = section_list.replace('\\', '')
                else:
                    section_list = lines[3].rstrip('\\')

                step_name = section_list
                section_call_counter += 1
                section_object_text = section_creation(step_name, section_call_counter)
                new_section_found = True
                # Call the section object function

            if 'SELECT_BUTTON' in lines or 'SELECT_RADIO' in lines:
                if checkbox_indicator:
                    q_a_call_counter += 1
                    question = 'Checkbox'
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary.clear()
                    checkbox_indicator = False
                lines = lines.split('"')
                question = lines[3].rstrip('\\')
                found_select_radio_button = True

            # Condition to capture answer:
            if found_select_radio_button is True:
                if r'<camunda:property name=\"options.' in lines:
                    lines = lines.split('"')
                    answer_label = lines[1].rstrip('\\')
                    answer_label = answer_label.replace('options.', '')
                    answer_label = answer_label.rstrip(answer_label[-1]).replace('.', '')
                    a_number += 1
                    a_number_string = 'answer' + str(a_number)
                    answer_dictionary[a_number_string] = answer_label
                if r'conditionalShowExpression' in lines:
                    lines = lines.split('"')
                    # This generates the tool tip for the question object
                    tooltip = tooltip_generator(lines)

                if '</camunda:properties>' in lines:
                    a_number = 0
                    q_a_call_counter += 1
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary.clear()
                    found_select_radio_button = False

            if 'YES_NO_QUESTION' in lines:
                if checkbox_indicator:
                    q_a_call_counter += 1
                    question = 'Checkbox'
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary.clear()
                    checkbox_indicator = False
                lines = lines.split('"')
                question = lines[3].rstrip('\\')
                answer_dictionary['answer1'] = 'Yes'
                answer_dictionary['answer2'] = 'No'
                yes_no_question_found = True

            if yes_no_question_found:
                if r'conditionalShowExpression' in lines:
                    lines = lines.split('"')
                    # This generates the tool tip for the question object
                    tooltip = tooltip_generator(lines)

                if '</camunda:properties>' in lines:
                    a_number = 0
                    q_a_call_counter += 1
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary.clear()
                    yes_no_question_found = False

            if r'"CHECKBOX\"' in lines:
                checkbox_indicator = True
                lines = lines.split('"')
                answer = lines[3].rstrip('\\')
                checkbox_count += 1
                answer_number = 'answer' + str(checkbox_count)
                answer_dictionary[answer_number] = answer
                found_checkbox = True

            if found_checkbox:
                if r'conditionalShowExpression' in lines:
                    lines = lines.split('"')
                    # This generates the tool tip for the question object
                    tooltip = tooltip_generator(lines)

                if '</camunda:properties>' in lines:
                    found_checkbox = False

            if r'"STRING\"' in lines:
                if checkbox_indicator:
                    q_a_call_counter += 1
                    question = 'Checkbox'
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary.clear()
                    checkbox_indicator = False
                lines = lines.split('"')
                question = lines[3].rstrip('\\')
                found_string_question = True

            if found_string_question:
                if r'conditionalShowExpression' in lines:
                    lines = lines.split('"')
                    # This generates the tool tip for the question object
                    tooltip = tooltip_generator(lines)
                if r'name=\"maxBoundary\"' in lines:
                    answer = lines.split('"')
                    answer = answer[3].rstrip('\\')
                    answer_dictionary['answer1'] = answer
                    q_a_call_counter += 1
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary = {}
                    found_string_question = False

            if 'SELECT_ONE' in lines:
                if checkbox_indicator:
                    q_a_call_counter += 1
                    question = 'Checkbox'
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary.clear()
                    checkbox_indicator = False
                lines = lines.split('"')
                question = lines[3].rstrip('\\')
                found_select_one_button = True

            # Condition to capture answer and answer ID:
            if found_select_one_button is True:
                if r'<camunda:property name=\"options.' in lines:
                    lines = lines.split('"')
                    answer_label = lines[1].rstrip('\\')
                    answer_label = answer_label.replace('options.', '')
                    answer_label = answer_label.rstrip(answer_label[-1]).replace('.', '')
                    a_number += 1
                    a_number_string = 'answer' + str(a_number)
                    answer_dictionary[a_number_string] = answer_label
                if r'conditionalShowExpression' in lines:
                    lines = lines.split('"')
                    # This generates the tool tip for the question object
                    tooltip = tooltip_generator(lines)
                if '</camunda:properties>' in lines:
                    a_number = 0
                    q_a_call_counter += 1
                    one_q_a_formation += objectCreate(question, answer_dictionary, q_a_call_counter, tooltip)
                    tooltip = ''
                    answer_dictionary.clear()
                    found_select_one_button = False
            if new_section_found:
                if counter_reset:
                    q_a_call_counter = 0
                    counter_reset = False

            if r'</bpmn:userTask>' in lines:
                if new_section_found:
                    # section_object_text to be replaced with the correct x-height of the section
                    new_height = int(q_y_position + height_box + 100)
                    section_object_text = section_object_text.replace('<replace_variable>', str(new_height))
                    xml_code += section_object_text + one_q_a_formation
                    section_object_text = ''
                    one_q_a_formation = ''
                    new_section_found = False
                    counter_reset = True


def idRandomizer():
    """
    Generates unique 20-character IDs for XML objects
    Returns:
        Unique random ID string
    """
    global random_id_list
    random_generated_id = ''
    for letter in range(0, 10):
        lower_upper_alphabet = string.ascii_letters
        random_letter = random.choice(lower_upper_alphabet)
        random_generated_id = random_generated_id + random_letter

    random_generated_id += random_generated_id + '--1'
    # Recursion call to the function if the ID generated is duplicate
    if random_generated_id in random_id_list:
        random_generated_id = idRandomizer()
    return random_generated_id


def section_creation(section_name, section_call_counter):
    """
    Creates XML structure for a new section
    Args:
        section_name: Name of the section
        section_call_counter: Counter for section positioning
    Returns:
        XML structure for the section
    """
    global section_object, section_object_id, section_x_pos, section_y_pos
    section_call_counter = section_call_counter
    section_name = section_name
    primary_canvas_id = 1
    section_object_id = idRandomizer()
    if section_call_counter == 1:
        section_x_pos = 210
        section_y_pos = 230
    elif section_call_counter > 1:
        section_x_pos += 200
        section_y_pos += 0
    section_object = f'<object label="{section_name}" stencilType="task" id="{section_object_id}"><mxCell style="shape=ext;rounded=1;html=1;whiteSpace=wrap;container=1;verticalAlign=top;" vertex="1" collapsed="1" parent="{primary_canvas_id}" rdfUpgraded="1" assetTypeVersion="3"><mxGeometry x="{section_x_pos}" y="{section_y_pos}" width="110" height="60" as="geometry"><mxPoint x="{section_x_pos}" y="{section_x_pos}" width="560" height="<replace_variable>" as="alternateBounds" /></mxGeometry><ResourceDescriptor resource="_:{section_object_id}" serialization-version="v0" as="resourceDescriptor"><SemanticDataContainer serialization-version="v0"><StringLiteral content="{section_object_id}" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/a2255956-c3df-4c2c-b489-c307f68abc97" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/84a80b5f-5642-4a17-9585-ebfdb65f4bec" property="https://ontology.security.amazon.dev/foundation/system-modeling/04539597-4283-4f65-8090-ae67f9d3e949" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/4f51991f-f3c6-4a47-9b00-013560ab92f4" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><IRI resource="https://ontology.security.amazon.dev/foundation/graph-structure/0b4eeac8-04e5-4e85-869c-bd56fb947b7b" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><StringLiteral content="Customer Data" property="http://www.w3.org/2000/01/rdf-schema#label" /><StringLiteral content="UnknownPage" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/05cc531c-d241-49c3-80dc-bd3777c5426f" /></SemanticDataContainer></ResourceDescriptor></mxCell></object>'
    return section_object


previous_height_increment = 0


def objectCreate(question, a_dict, q_a_call_counter, tooltip):
    """
    Creates XML structure for question-answer pairs
    Args:
        question: Question text
        a_dict: Dictionary of answers
        q_a_call_counter: Counter for positioning
        tooltip: Tooltip text for conditional logic
    Returns:
        Combined XML structure for question and answers
    """
    global question_object, answer_object, section_object_id, q_x_position, q_y_position, a_x_position, a_y_position, one_q_a_formation, previous_height_increment, height_box
    answer_dictionary = a_dict
    answers = ''
    height_box = 60
    box_length_var = len(answer_dictionary.keys())
    length_check = 0
    height_increment = 0
    if box_length_var > 3:
        height_box = 20 * int(box_length_var)

    additional_height_increment = height_box - 60
    if previous_height_increment > 0:
        height_increment = previous_height_increment

    tooltip = tooltip
    q_a_call_counter = q_a_call_counter
    if q_a_call_counter == 1:
        q_x_position = 20
        q_y_position = 100
        a_x_position = 280
        a_y_position = 100
    elif q_a_call_counter > 1:
        q_x_position += 0
        q_y_position += 80 + height_increment
        a_x_position += 0
        a_y_position += 80 + height_increment
    question_object_id = idRandomizer()
    if tooltip != '':
        question_object = f'<object label="{question}" stencilType="generic-component" tooltip="{tooltip}" id="{question_object_id}"><mxCell style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="{section_object_id}" rdfUpgraded="1" assetTypeVersion="3"><mxGeometry x="{q_x_position}" y="{q_y_position}" width="250" height="{height_box}" as="geometry" /><ResourceDescriptor resource="_:{question_object_id}" serialization-version="v0" as="resourceDescriptor"><SemanticDataContainer serialization-version="v0"><StringLiteral content="{question_object_id}" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/a2255956-c3df-4c2c-b489-c307f68abc97" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/84a80b5f-5642-4a17-9585-ebfdb65f4bec" property="https://ontology.security.amazon.dev/foundation/system-modeling/04539597-4283-4f65-8090-ae67f9d3e949" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/4f51991f-f3c6-4a47-9b00-013560ab92f4" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><IRI resource="https://ontology.security.amazon.dev/foundation/graph-structure/0b4eeac8-04e5-4e85-869c-bd56fb947b7b" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><StringLiteral content="What is the type of customer?" property="http://www.w3.org/2000/01/rdf-schema#label" /><StringLiteral content="UnknownPage" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/05cc531c-d241-49c3-80dc-bd3777c5426f" /></SemanticDataContainer></ResourceDescriptor></mxCell></object>'
    else:
        tooltip = "Mandate"
        question_object = f'<object label="{question}" stencilType="generic-component" tooltip="{tooltip}" id="{question_object_id}"><mxCell style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="{section_object_id}" rdfUpgraded="1" assetTypeVersion="3"><mxGeometry x="{q_x_position}" y="{q_y_position}" width="250" height="{height_box}" as="geometry" /><ResourceDescriptor resource="_:{question_object_id}" serialization-version="v0" as="resourceDescriptor"><SemanticDataContainer serialization-version="v0"><StringLiteral content="{question_object_id}" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/a2255956-c3df-4c2c-b489-c307f68abc97" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/84a80b5f-5642-4a17-9585-ebfdb65f4bec" property="https://ontology.security.amazon.dev/foundation/system-modeling/04539597-4283-4f65-8090-ae67f9d3e949" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/4f51991f-f3c6-4a47-9b00-013560ab92f4" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><IRI resource="https://ontology.security.amazon.dev/foundation/graph-structure/0b4eeac8-04e5-4e85-869c-bd56fb947b7b" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><StringLiteral content="What is the type of customer?" property="http://www.w3.org/2000/01/rdf-schema#label" /><StringLiteral content="UnknownPage" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/05cc531c-d241-49c3-80dc-bd3777c5426f" /></SemanticDataContainer></ResourceDescriptor></mxCell></object>'
    answer_object_id = idRandomizer()
    pre_answer = '&lt;div&gt;'
    post_answer = '&lt;/div&gt;'
    for key, value in answer_dictionary.items():
        answers += f'{pre_answer}{value}{post_answer}'
    answer_object = f'<object label="{answers}" stencilType="generic-component" id="{answer_object_id}"><mxCell style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="{section_object_id}" rdfUpgraded="1" assetTypeVersion="3"><mxGeometry x="{a_x_position}" y="{a_y_position}" width="250" height="{height_box}" as="geometry" /><ResourceDescriptor resource="_:{answer_object_id}" serialization-version="v0" as="resourceDescriptor"><SemanticDataContainer serialization-version="v0"><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/4f51991f-f3c6-4a47-9b00-013560ab92f4" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><IRI resource="https://ontology.security.amazon.dev/foundation/graph-structure/0b4eeac8-04e5-4e85-869c-bd56fb947b7b" property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type" /><IRI resource="https://ontology.security.amazon.dev/design-inspector/components/84a80b5f-5642-4a17-9585-ebfdb65f4bec" property="https://ontology.security.amazon.dev/foundation/system-modeling/04539597-4283-4f65-8090-ae67f9d3e949" /><StringLiteral content="xr8A-sJWZigq67Yn0gtEn" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/05cc531c-d241-49c3-80dc-bd3777c5426f" /><StringLiteral content="NCVCNA" property="http://www.w3.org/2000/01/rdf-schema#label" /><StringLiteral content="{answer_object_id}" property="https://ontology.security.amazon.dev/foundation/diagram-visualization/a2255956-c3df-4c2c-b489-c307f68abc97" /></SemanticDataContainer></ResourceDescriptor></mxCell></object>'
    q_a_text = question_object + answer_object
    previous_height_increment = additional_height_increment
    return q_a_text


# Main execution flow
readingXMLFile()

# Final XML assembly and file output
endText = '</root></mxGraphModel>'
xml_output = initial_xml_code + xml_code + endText

# Write the final XML to output file
f = open("di_output.xml", "w", encoding='UTF-8')
f.write(xml_output)
f.close()

