from typing import Any, TypedDict
from dotenv import load_dotenv
import os
import json
import openai


load_dotenv()
class Params(TypedDict):
    pass


class Result(TypedDict):
    is_correct: bool
# A basic way to call ChatGPT from the Lambda Feedback platform


def enforce_full_stop(s):
    if not s.endswith('.'):
        s += '.'
    return s


def evaluation_function(response, answer, parameters):
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - 'response' which contains the student's answer
    - 'parameters' is a dictionary which contains the parameters:
        - 'model'
        - 'question_prompt' 
        - 'default_prompt'

    The output of this function is what is returned as the API response 
    and therefore must be JSON-encodable. It must also conform to the 
    response schema.

    Any standard python library may be used, as well as any package 
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or 
    split into many) is entirely up to you. All that matters are the 
    return types and that evaluation_function() is the main function used 
    to output the evaluation response.
    """
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    

    # Question prompt is required
    if parameters['question_prompt'] and str(parameters['question_prompt']) != "0":
        question_prompt = enforce_full_stop(parameters['question_prompt'])
    else:
        question_prompt = enforce_full_stop("Write a descriptive piece with the title 'A Room with a View' as suggested by an image provided to them")
    
    # Setting default prompt, not required necessarily
    default_prompt = enforce_full_stop("Pretend like you are an experienced GCSE English teacher. Your year 10 student has written a response to a GCSE descriptive task of an image. Remember that it is a descriptive task. If the student has written a narrative piece, gently remind them that they need to focus on setting the scene, not creating a story. Focus on the following two broad areas; content and technical accuracy. For technical accuracy, comment on four of the following: sentence demarcation, punctuation, sentence forms, grammar, spelling and vocabulary. Please pick these four sections appropriately; giving praise (specific things the student has done well) on two of them and targets (specific things the student can improve) on the other two. Use headings to show clear demarcation of ideas. Make sure to provide critical feedback, specifically picking out literary devices that may have been misused. Make sure you only give 2 pieces of praise and only 2 pieces of targets. For content and organisation skills, comment on four of the following: Communication, Tone, style, register, Vocabulary and devices, Structural features, Ideas, Cohesion (paragraphs, linking devices). Please pick these four sections appropriately; giving praise (specific things the student has done well) on two of them and targets (specific things the student can improve) on the other two. Use headings to show clear demarcation of ideas. Make sure you only give 2 pieces of praise and only 2 pieces of targets. When giving students feedback on their content, make sure to use open-ended questions (instead of “use shorter lines in this paragraph”, say “have you considered rephrasing this paragraph to” and then give them an example of how it should look). If you think a student has written a narrative piece instead of a descriptive piece, mention it and gently prompt them into thinking about the different smells, sounds or feels that they would experience in that setting. End the response with either “Great job, keep writing!” or “Keep up the good work!” ")
    if 'default_prompt' in parameters:
        # NOTE: if it is in parameters & it is not empty or not 0, then overwrite the default prompt
        if parameters['default_prompt'] and str(parameters['default_prompt']) != "0":
            default_prompt = enforce_full_stop(parameters['default_prompt'])

    # Call openAI API for boolean
    completion_boolean = openai.ChatCompletion.create(
        model=parameters['model'],
        messages=[{"role": "system", "content": question_prompt + " " + default_prompt},
                  {"role": "user", "content": response}])

    is_correct = completion_boolean.choices[0].message.content.strip(
    ) == "True"
    is_correct_str = str(is_correct)

    output = {"is_correct": is_correct}

    # Check if feedback prompt is empty or not. Only populates feedback in 'output' if there is a 'feedback_prompt'.
    completion_feedback = openai.ChatCompletion.create(
        model=parameters['model'],
        messages=[{"role": "system", "content": "Students have been asked to do the following task: " +question_prompt + " " + default_prompt+  " \n\nGive objective feedback. You must take the student's answer to be: " + is_correct_str},
                    {"role": "user", "content": response}])

    feedback = completion_feedback.choices[0].message.content.strip()
    output["feedback"] = feedback

    # print(output)

    return output