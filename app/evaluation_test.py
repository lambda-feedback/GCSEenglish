import time
import unittest

from dotenv import load_dotenv
import os
load_dotenv()

try:
    from .evaluation import Params, evaluation_function
except ImportError:
    from evaluation import Params, evaluation_function

model = 'gpt-4o-mini'
default_prompt = "Output a Boolean: True if the student is correct and False if the student is incorrect"
answer = 1

class TestEvaluationFunction(unittest.TestCase):

    def setUp(self):
        time.sleep(2)

    def test_general_risk(self):
        response = "The pressurised vessel, because it could explode and cause injury if it's overpressurised."
        parameters = {'model': model,
                      'question_prompt': "The student needs to enter a risk with a short description of how it can cause harm",
                      'default_prompt': default_prompt}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output['is_correct'], True)

    def test_photosynthesis_definition_correct(self):
        response = "Photosynthesis is the process by which plants convert light energy into chemical energy to fuel their growth."
        parameters = {'model': model,
                      'question_prompt': "Evaluate the student's response for the definition of photosynthesis",
                      'default_prompt': default_prompt}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output["is_correct"], True)

    def test_photosynthesis_definition_incomplete(self):
        response = "Photosynthesis is the process by which plants make their food."
        parameters = {'model': model,
                      'question_prompt': "Evaluate the student's response for the definition of photosynthesis. They should mention the conversion of light energy to chemical energy.",
                    #   'feedback_prompt': feedback_prompt,
                      'default_prompt': default_prompt}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output["is_correct"], False)

    def test_capital_city_incorrect(self):
        response = "The capital of France is Berlin."
        parameters = {'model': model,
                      'question_prompt': "Analyze the response regarding the capital of France",
                    #   'feedback_prompt': feedback_prompt,
                      'default_prompt': default_prompt}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output["is_correct"], False)

    def test_list(self):
        response = "Red, blue and yellow."
        parameters = {'model': model,
                      'question_prompt': "Mark this response asking students for the three primary colours in painting.",
                      'default_prompt': default_prompt}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output["is_correct"], True)

    def test_physics_definition(self):
        response = "The law of conservation of energy states that energy cannot be created or destroyed, only transformed from one form to another. It's a fundamental principle in physics."
        parameters = {'model': model,
                      'question_prompt': "Examine the explanation of the law of conservation of energy and provide feedback.",
                      'default_prompt': default_prompt}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output["is_correct"], True)

    def test_internal_prompt(self):
        response = """The room feels like a sanctuary, its spacious interior bathed in the golden light of a tranquil morning. The walls, painted in a soft shade of blue reminiscent of the sky at dawn, create an atmosphere of calm, while a subtle scent of fresh lavender lingers in the air, blending harmoniously with the occasional breeze wafting in through the open window. A plush, cream-colored rug muffles footsteps, its thick fibers soft underfoot, while the rich texture of a velvet armchair beckons you to sink in and unwind. The sturdy oak bookshelf nearby is a quiet testament to the room’s inhabitant, its shelves brimming with well-loved novels and tiny trinkets that hint at distant travels.

        Through the wide window, the garden unfolds like a living painting. Vibrant flowers in full bloom dot the emerald expanse, their fragrance mingling with the earthy scent of the small pond at the center, which glistens under the sun’s rays. The cheerful chirping of birds blends with the gentle rustling of leaves, creating a symphony that feels both timeless and alive. During sunny mornings, the light floods the room with warmth, while on rainy afternoons, droplets dance on the glass, casting shifting patterns of shadow and light across the room.

        Together, the indoor space and the view form an intimate dialogue, each enhancing the other’s beauty. Sitting here, you’re enveloped by a profound sense of peace, as though time itself has paused. It’s a place where you could lose yourself in a book, daydream endlessly, or simply sit in quiet reflection, letting the serenity seep into your soul."""
        parameters = {'model': model,
                      'question_prompt': "",
                      'default_prompt': ""}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output["is_correct"], False) # TODO: find a response that passes and set the assert to True

    def test_internal_no_default_prompt(self):
        response = "test"
        parameters = {'model': model,
                      'question_prompt': ""}
        output = evaluation_function(response, answer, parameters)
        self.assertEqual(output["is_correct"], False)
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    
        def test_returns_is_correct_true(self):
        response, answer, params = None, None, Params()
        result = evaluation_function(response, answer, params)

        self.assertEqual(result.get("is_correct"), True)
    """



if __name__ == "__main__":
    unittest.main()
