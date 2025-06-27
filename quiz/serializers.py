from rest_framework import serializers
from .models import Test, Question, UserAnswer


class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода вопроса без правильных ответов.
    """
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'choices']


class UserAnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сохранения ответа пользователя на вопрос.
    """
    class Meta:
        model = UserAnswer
        fields = ['question', 'answer']

    def validate(self, data):
        """
        Дополнительная валидация в зависимости от типа вопроса.
        """
        question = data.get("question")
        answer = data.get("answer")

        if question.question_type == Question.TEXT:
            if not isinstance(answer, str):
                raise serializers.ValidationError("Ответ должен быть строкой для текстового вопроса.")
        elif question.question_type in (Question.SINGLE, Question.MULTIPLE):
            if not isinstance(answer, list):
                raise serializers.ValidationError("Ответ должен быть списком.")
            if not all(a in question.choices for a in answer):
                raise serializers.ValidationError("Один или более выбранных ответов отсутствуют в списке вариантов.")
        return data


class TestWithAnswersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения теста с ответами текущего пользователя.
    """
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'questions']

    def get_questions(self, obj):
        """
        Возвращает список вопросов с прикрепленными ответами пользователя, если они есть.
        """
        user = self.context['request'].user
        data = []

        user_answers = {
            ua.question_id: ua.answer
            for ua in UserAnswer.objects.filter(user=user, question__test=obj)
        }

        for q in obj.questions.all():
            data.append({
                'id': q.id,
                'text': q.text,
                'question_type': q.question_type,
                'choices': q.choices,
                'user_answer': user_answers.get(q.id)
            })
        return data
