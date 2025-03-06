# Script to generate Payload code for paramount BPMN process
# This script processes BPMN XML and generates a JavaScript structure for form handling

from openpyxl import Workbook
from openpyxl import load_workbook

# Initialize global variables
xml_string = '' # Stores formatted XML content
dict_string = 'var top_structure = [\n[' # Stores the JavaScript structure being built


def readingXMLFile():
    """
    Reads and formats the BPMN XML file for better processing
    1. Reads the original XML file
    2. Reformats it with proper line breaks after '>' characters
    3. Saves the formatted XML back to file
    4. Initiates data extraction
    """
    global xml_string
    line = ''
    # Read and format XML file for better alignment
    location = 'bpmn-digital.txt'
    with open(file=location, encoding="utf-8", mode='r') as xml_file:
        for lines in xml_file:
            for words in lines:
                if words != '>':
                    line += words
                if words == '>':
                    line = line + '>'
                    xml_string += line + '\n'
                    line = ''
        xml_file.close()

    with open(file='bpmn-digital.txt', encoding="utf-8", mode='w') as f:
        f.write(xml_string)
        f.close()
    # Save formatted XML back to file

    extractingData()


def answer_extraction():
    """
    Placeholder function for answer extraction
    Currently not implemented
    """
    with open(file='bpmn-digital.txt', encoding='utf-8', mode = 'r') as xml_file:
        for lines in xml_file:
            lines = str(lines)
    
    
def extractingData():
    """
    Main function to extract form data from BPMN XML
    Processes different types of form fields:
    - SELECT_BUTTON/RADIO
    - YES_NO_QUESTION
    - SELECT_ONE
    - CHECKBOX
    
    Creates a structured JavaScript object containing:
    - Questions
    - Question IDs
    - Answer types
    - Answer options
    - Section information
    """
    global xml_string, dict_string
    step = ''
    stop_clock = 0
    question = ''
    question_id = ''
    step = ''
    section_name = ''
    scriptEscape = False
    found_initial = False
    initial_section_found = 0
    prev_section = ''
    answer_type_button = False
    with open(file='bpmn-digital.txt', encoding='utf-8', mode='r') as xml_file:
        for lines in xml_file:
            lines = str(lines)
            
            # Skip script tasks
            if 'scriptTask id' in lines:
                scriptEscape = True
                continue
            if r'</bpmn:scriptTask>' in lines:
                scriptEscape = False
                continue
            if scriptEscape:
                continue
            
            # Process user tasks - extract section information
            if '<bpmn:userTask id=' in lines:
                # Process task ID and section name
                # Handle special cases like VIP sections and formatting
                found_initial = True
                lines = lines.split('"')
                task_id = lines[1]
                task_id = task_id.rstrip('\\')
                task_id = task_id.lower()
                section_list = lines[3].split(' ')
                step_name = ''
                if '&#10;_VIP' in lines[3]:
                    section_list = lines[3].rstrip('&#10;_VIP\\')
                elif '&#10;' in lines[3]:
                    section_list = lines[3].replace('&#10;', '')
                    section_list = section_list.replace('\\', '')
                else:
                    section_list = lines[3].rstrip('\\')
                section_name = section_list
                section_name = section_name.replace('&#38;', '&')
                section_list = section_list.split(' ')
                
                for names in section_list:
                    names = names.strip(" ")
                    step_name += names + '_'
                step_name = step_name.lower()
                step_name = step_name + task_id
                step_name = step_name.replace('&#38;', '&')

                if initial_section_found == 1:
                    if prev_section != step_name and step_name != '':
                        dict_string += '\n],\n['
                        prev_section = step_name
                    prev_section = step_name
                if initial_section_found == 0:
                    prev_section = step_name
                    initial_section_found = 1

            # Process different question types
            if 'SELECT_BUTTON' in lines or 'SELECT_RADIO' in lines:
                # Handle select/radio button questions
                lines = lines.split('"')
                question_id = lines[1].rstrip('\\')
                question = lines[3].rstrip('\\')
                question = question.replace('&#39;', "")
                question = question.replace('&#34;', "")
                question = question.replace('&#38;', '&')
                type_ans = "string"
                answer_list = '['
                answer_type_button = True
            if 'YES_NO_QUESTION' in lines:
                # Handle Yes/No questions
                lines = lines.split('"')
                question_id = lines[1].rstrip('\\')
                question = lines[3].rstrip('\\')
                question = question.replace('&#39;', "")
                question = question.replace('&#34;', "")
                question = question.replace('&#38;', '&')
                type_ans = "bool"
                answer_list = '[{"False":"No"}, {"True":"Yes"}]'
                js_dict(prev_section, step_name, question, question_id, type_ans, section_name, answer_list)
            if 'SELECT_ONE' in lines:
                # Handle single select questions
                lines = lines.split('"')
                question_id = lines[1].rstrip('\\')
                question = lines[3].rstrip('\\')
                question = question.replace('&#39;', "")
                question = question.replace('&#34;', "")
                question = question.replace('&#38;', '&')
                type_ans = "string"
                answer_list = '['
                answer_type_button = True
            if 'CHECKBOX' in lines:
                # Handle checkbox questions
                lines = lines.split('"')
                question_id = lines[1].rstrip('\\')
                question = lines[3].rstrip('\\')
                question = question.replace('&#39;', "")
                question = question.replace('&#34;', "")
                question = question.replace('&#38;', '&')
                type_ans = "bool"
                answer_list = '[{"false":"No"}, {"true":"Yes"}]'
                js_dict(prev_section, step_name, question, question_id, type_ans, section_name, answer_list)

            if answer_type_button:
                # Extract and format answer options
                if '"options.' in lines:
                    split_text = lines.split('\\"')
                    answer_var = split_text[3]
                    answer_label = split_text[1].replace("options.", "")
                    answer_label = answer_label[:-2]
                    answer_list += '{"' + answer_var + '":"' + answer_label + '"}, '
                if '</camunda:properties>' in lines:
                    answer_list += ']'
                    js_dict(prev_section, step_name, question, question_id, type_ans, section_name, answer_list)
                    answer_type_button = False
                    answer_list = ''
            if lines == 'bpmn:definitions>"':
                found_initial = False
                if found_initial is False:
                    stop_clock += 1
                    if stop_clock > 10:
                        break
                    
    # Finalize the JavaScript structure
    dict_string += '\n]\n]'
    print("Payload generated and saved in the file 'aa2.js'")
    with open('aa2.js', mode='w', encoding="utf-8") as js_file:
        js_file.write(dict_string)
        js_file.close()


def js_dict(prev_section, step_name, question, question_id, type_ans, section_name, answer_list):
    """
    Creates a JavaScript dictionary structure for each question
    Args:
        prev_section: Previous section idendentifier
        step_name: Current step name
        question: Question text
        question_id: Question identifier
        type_ans: Answer type
        section_name: Section name
        answer_list: List of possible answers
    """
    global dict_string
    if prev_section == step_name:
        if question != '':
            # Build dictionary structure with question details
            dict_string += '\n{ q_label: "' + question + '",\n'  # Adding question string
            dict_string += 'q_id: "' + question_id + '",\n'  # Adding question id
            dict_string += ' stepID: "' + prev_section + '",\n'  # Adding question string
            dict_string += ' type: "' + type_ans + '",\n'  # Adding question string
            dict_string += ' answer_label: ' + answer_list + ',\n'
            dict_string += ' stepName: "' + section_name + '"\n},'  # Adding stepname string


readingXMLFile()


"""JS Integration Code


var queue = document.get("queue_id").stringValue();
var marketplaceID = document.get("marketplace_id").stringValue();
var workflow_version = 18;
marketplaceID = parseInt(marketplaceID);

var workflow_answers = ionSystem.newEmptyList();
var outputPayload = ionSystem.newEmptyStruct();

let time_Stamp = new Date().toISOString();
outputPayload.put('workflow_version').newInt(workflow_version);
outputPayload.put('time_Stamp').newString(time_Stamp);
outputPayload.put("queue").newString(queue);
outputPayload.put("marketplaceID").newInt(marketplaceID)

function sectionLoopStruct(label, stepID, stepName, questionID, answer, answer_label) {
    var question_struct = ionSystem.newEmptyStruct();
    question_struct.put("questionId").newString(questionID);
    question_struct.put("questionText").newString(label);
    question_struct.put("answer").newString(answer);
    question_struct.put("answer_label").newString(answer_label);
    question_struct.put("stepId").newString(stepID);
    question_struct.put("stepName").newString(stepName);
    workflow_answers.add(question_struct);
};

function questionFilter() {
    // --Consolidating all data--//
    for (var section = 0; section < top_structure.length; section++) {
        for (var questions = 0; questions < top_structure[section].length; questions++) {
            var questionLabel = top_structure[section][questions]["q_label"];
            var type = top_structure[section][questions]["type"];
            var stepID = top_structure[section][questions]["stepID"];
            var stepName = top_structure[section][questions]["stepName"];
            var questionID = top_structure[section][questions]["q_id"];
            var answer = "";

            function answerDefine(q_id) {
                return (answer = document.get(q_id).stringValue());
            }

            if (type === "bool") {
                questionID = questionID + questionID;
                if (document.get(questionID) === null) {
                    continue;
                } else {
                    answer = answerDefine(questionID);
                }
            } else {
                if (document.get(questionID) === null) {
                    continue;
                } else {
                    answer = answerDefine(questionID);
                }
            }

            for (var i = 0; i < top_structure[section][questions]["answer_label"].length; i++) {
                var answerLabelObj = top_structure[section][questions]["answer_label"][i];
                var answerLabelKey = Object.keys(answerLabelObj)[0];
                if (answer === answerLabelKey) {
                    var answer_label = answerLabelObj[answerLabelKey]
                }
            }
            if (answer_label === null) {
                continue
            }
            else {
                sectionLoopStruct(questionLabel, stepID, stepName, questionID, answer, answer_label);
            }
        }
    }
    // --Consolidating all data end--//
};

questionFilter();

outputPayload.put("answers", workflow_answers);
var retVal = ionSystem.newEmptyStruct();
retVal.put("outputPayload", outputPayload);
retVal;



**********************   --- SUBPROCESS (Below) ---   **********************

var payload_subprocess = ionSystem.newEmptyStruct();
var workflow_answers = ionSystem.newEmptyList();

function sectionLoopStruct(label, stepID, stepName, questionID, answer, answer_label) {
    var question_struct = ionSystem.newEmptyStruct();
    question_struct.put("questionId").newString(questionID);
    question_struct.put("questionText").newString(label);
    question_struct.put("answer").newString(answer);
    question_struct.put("answer_label").newString(answer_label);
    question_struct.put("stepId").newString(stepID);
    question_struct.put("stepName").newString(stepName);
    workflow_answers.add(question_struct);
};

function questionFilter() {
    // --Consolidating all data--//
    for (var section = 0; section < top_structure.length; section++) {
        for (var questions = 0; questions < top_structure[section].length; questions++) {
            var questionLabel = top_structure[section][questions]["q_label"];
            var type = top_structure[section][questions]["type"];
            var stepID = top_structure[section][questions]["stepID"];
            var stepName = top_structure[section][questions]["stepName"];
            var questionID = top_structure[section][questions]["q_id"];
            var answer = "";

            function answerDefine(q_id) {
                return (answer = document.get(q_id).stringValue());
            }

            if (type === "bool") {
                questionID = questionID + questionID;
                if (document.get(questionID) === null) {
                    continue;
                } else {
                    answer = answerDefine(questionID);
                }
            } else {
                if (document.get(questionID) === null) {
                    continue;
                } else {
                    answer = answerDefine(questionID);
                }
            }

            for (var i = 0; i < top_structure[section][questions]["answer_label"].length; i++) {
                var answerLabelObj = top_structure[section][questions]["answer_label"][i];
                var answerLabelKey = Object.keys(answerLabelObj)[0];
                if (answer === answerLabelKey) {
                    var answer_label = answerLabelObj[answerLabelKey]
                }
            }
            if (answer_label === null) {
                continue
            }
            else {
                sectionLoopStruct(questionLabel, stepID, stepName, questionID, answer, answer_label);
            }
        }
    }
    // --Consolidating all data end--//
};

questionFilter();


payload_subprocess.put("answers", workflow_answers);
var retVal = ionSystem.newEmptyStruct();
retVal.put("payload_subprocess", payload_subprocess);
retVal;"""
