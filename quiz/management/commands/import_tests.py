import csv
import json
from django.core.management.base import BaseCommand
from quiz.models import Test, Question


class Command(BaseCommand):
    help = 'Импортирует тесты из CSV-файла.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь до CSV-файла.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    test, _ = Test.objects.get_or_create(title=row['test_title'])

                    try:
                        choices = json.loads(row['choices']) if row.get('choices') else None
                        correct_answers = json.loads(row['correct_answers'])

                        if row['question_type'] not in dict(Question.TYPE_CHOICES):
                            self.stderr.write(self.style.ERROR(
                                f"Неверный тип вопроса: {row['question_type']}, строка пропущена."
                            ))
                            continue

                        Question.objects.create(
                            test=test,
                            text=row['question_text'],
                            question_type=row['question_type'],
                            choices=choices,
                            correct_answers=correct_answers
                        )
                    except json.JSONDecodeError:
                        self.stderr.write(self.style.ERROR(f"Ошибка JSON в строке: {row}"))
                        continue

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Файл не найден: {file_path}"))
            return

        self.stdout.write(self.style.SUCCESS('Импорт завершён успешно.'))
