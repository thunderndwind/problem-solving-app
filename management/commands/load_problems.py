from django.core.management.base import BaseCommand
from problem_solving.models import Problem

class Command(BaseCommand):
    help = 'Loads predefined problems into the database'

    def handle(self, *args, **kwargs):
        problems = [
            {
                'title': 'Sum of Two Numbers',
                'description': 'Write a function that takes two integers as input and returns their sum.',
                'example_input': '5 7',
                'example_output': '12',
                'test_cases': [
                    {'input': '5 7', 'output': '12'},
                    {'input': '10 15', 'output': '25'},
                    {'input': '-5 9', 'output': '4'},
                    {'input': '0 0', 'output': '0'}
                ]
            },
            {
                'title': 'Reverse a String',
                'description': 'Write a function that takes a string as input and returns the string reversed.',
                'example_input': 'hello',
                'example_output': 'olleh',
                'test_cases': [
                    {'input': 'hello', 'output': 'olleh'},
                    {'input': 'world', 'output': 'dlrow'},
                    {'input': 'Python', 'output': 'nohtyP'},
                    {'input': 'a', 'output': 'a'}
                ]
            }
        ]

        for problem_data in problems:
            Problem.objects.create(
                title=problem_data['title'],
                description=problem_data['description'],
                example_input=problem_data['example_input'],
                example_output=problem_data['example_output'],
                test_cases=problem_data['test_cases']
            )
        self.stdout.write(self.style.SUCCESS('Successfully loaded problems'))
