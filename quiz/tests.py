from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Test, Question, UserAnswer
from django.core.management import call_command
from io import StringIO
from rest_framework.response import Response


class ModelTestCase(TestCase):
    """Тесты моделей: Test, Question и UserAnswer."""

    def setUp(self) -> None:
        """Создание тестового пользователя, теста и вопроса."""
        self.test = Test.objects.create(title='Sample Test')
        self.question = Question.objects.create(
            test=self.test,
            text='Sample Question',
            question_type=Question.SINGLE,
            choices=["A", "B"],
            correct_answers=["A"]
        )
        self.user = User.objects.create_user(username='user', password='pass')

    def test_question_str(self) -> None:
        """Проверка строкового представления Question."""
        self.assertIn('Sample Test', str(self.question))

    def test_user_answer(self) -> None:
        """Проверка строкового представления UserAnswer."""
        answer = UserAnswer.objects.create(user=self.user, question=self.question, answer=["A"])
        expected_str = f"Answer by {self.user.username} to Question {self.question.id}"
        self.assertEqual(str(answer), expected_str)


class ImportCommandTestCase(TestCase):
    """Тест команды импорта CSV-файла с тестами и вопросами."""

    def test_import_tests_command(self) -> None:
        """Проверка успешного выполнения команды `import_tests`."""
        csv_content = (
            "test_title,question_text,question_type,choices,correct_answers\n"
            "Test1,What is 2+2?,single,\"[\\\"2\\\", \\\"4\\\"]\",\"[\\\"4\\\"]\"\n"
        )
        csv_file = StringIO(csv_content)
        csv_file.name = 'test_data.csv'
        out = StringIO()

        call_command('import_tests', csv_file.name, stdout=out)
        self.assertIn('Импорт завершён успешно.', out.getvalue())


class APITestCase(TestCase):
    """Тесты API: вопросы, ответы и отправка теста."""

    def setUp(self) -> None:
        """Создание пользователя, клиента и тестовых данных."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='pass')
        self.test = Test.objects.create(title='API Test')

        for i in range(7):
            Question.objects.create(
                test=self.test,
                text=f'Q{i}',
                question_type=Question.SINGLE,
                choices=["A", "B"],
                correct_answers=["A"]
            )

        self.client.login(username='apiuser', password='pass')

    def test_questions_pagination(self) -> None:
        """Проверка пагинации вопросов по тесту (3 на страницу)."""
        response: Response = self.client.get(f'/api/test/{self.test.id}/questions/?page_size=3')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 3)

    def test_save_answer(self) -> None:
        """Проверка сохранения ответа пользователя на вопрос."""
        question = self.test.questions.first()
        response: Response = self.client.post(
            '/api/answer/', {"question": question.id, "answer": ["A"]}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'saved')

    def test_submit_test(self) -> None:
        """Проверка завершения теста и подсчета правильных ответов."""
        for question in self.test.questions.all():
            UserAnswer.objects.create(user=self.user, question=question, answer=["A"])

        response: Response = self.client.post(f'/api/submit/{self.test.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['correct'], 7)
