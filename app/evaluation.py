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
        - 'main_prompt' 
        - 'feedback_prompt'  
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
    

    # Making sure that each prompt ends with a full stop (prevents gpt getting confused when concatenated)
    main_prompt = enforce_full_stop(parameters['main_prompt'])
    default_prompt = enforce_full_stop(parameters['default_prompt'])
    feedback_prompt = enforce_full_stop(parameters['feedback_prompt'])
    print(main_prompt)
    print(feedback_prompt)

    # Call openAI API for boolean
    completion_boolean = openai.ChatCompletion.create(
        model=parameters['model'],
        messages=[{"role": "system", "content": main_prompt + " " + default_prompt},
                  {"role": "user", "content": response}])

    is_correct = completion_boolean.choices[0].message.content.strip(
    ) == "True"
    is_correct_str = str(is_correct)

    output = {"is_correct": is_correct}

    # Check if feedback prompt is empty or not. Only populates feedback in 'output' if there is a 'feedback_prompt'.
    if parameters['feedback_prompt'].strip():
        completion_feedback = openai.ChatCompletion.create(
            model=parameters['model'],
            messages=[{"role": "system", "content": main_prompt + " " + feedback_prompt + " You must take the student's answer to be: " + is_correct_str},
                      {"role": "user", "content": response}])

        feedback = completion_feedback.choices[0].message.content.strip()
        output["feedback"] = feedback

    return output
<<<<<<< HEAD
print("test")
=======
    print("test")

>>>>>>> a52bf76363fb232fc900e2d33910ac47e9562f86
