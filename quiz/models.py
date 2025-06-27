from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    """
    Модель теста, содержащая уникальное название.
    """
    title: str = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    """
    Модель вопроса, связанного с тестом.
    Поддерживаются типы: текстовый, один выбор, несколько выборов.
    """
    TEXT = 'text'
    SINGLE = 'single'
    MULTIPLE = 'multiple'

    TYPE_CHOICES = [
        (TEXT, 'Text'),
        (SINGLE, 'Single Choice'),
        (MULTIPLE, 'Multiple Choice'),
    ]

    test: Test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text: str = models.TextField()
    question_type: str = models.CharField(max_length=10, choices=TYPE_CHOICES)
    choices: list | None = models.JSONField(blank=True, null=True, help_text="Список вариантов ответа, если применимо")
    correct_answers: list = models.JSONField(help_text="Список правильных ответов (строки или индексы)")

    def __str__(self) -> str:
        return f"Question {self.id} for Test '{self.test.title}'"


class UserAnswer(models.Model):
    """
    Модель ответа пользователя на вопрос.
    Позволяет сохранить незавершенные тесты (через флаг `completed`).
    """
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    question: Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer: list = models.JSONField(help_text="Ответ пользователя (список значений)")
    completed: bool = models.BooleanField(default=False, help_text="Флаг завершения теста")

    def __str__(self) -> str:
        return f"Answer by {self.user.username} to Question {self.question.id}"
