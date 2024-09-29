from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()  # Problem statement
    example_input = models.TextField()
    example_output = models.TextField()
    test_cases = models.JSONField()  # Stores test cases as a JSON object (input/output pairs)

    def __str__(self):
        return self.title

class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()  # Python code submitted by the user
    passed = models.BooleanField(default=False)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solution by {self.user.username} for {self.problem.title}"
