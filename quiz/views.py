from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import Test, UserAnswer
from .serializers import QuestionSerializer, TestWithAnswersSerializer, UserAnswerSerializer
from rest_framework.pagination import PageNumberPagination


class QuestionPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class TestQuestionsView(generics.RetrieveAPIView):
    """
    Получение списка вопросов конкретного теста (без учета пользователя).
    """
    queryset = Test.objects.all()
    serializer_class = QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        test = self.get_object()
        questions = test.questions.all().order_by('id')
        paginator = QuestionPagination()
        page = paginator.paginate_queryset(questions, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TestWithUserAnswersView(generics.RetrieveAPIView):
    """
    Получение теста с уже введенными ответами текущего пользователя.
    """
    queryset = Test.objects.all()
    serializer_class = TestWithAnswersSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class SaveAnswerView(generics.CreateAPIView):
    """
    Сохранение или обновление ответа пользователя на конкретный вопрос.
    """
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = serializer.validated_data['question'].id
        answer = serializer.validated_data['answer']

        UserAnswer.objects.update_or_create(
            user=request.user,
            question_id=question_id,
            defaults={'answer': answer}
        )
        return Response({'status': 'saved'}, status=status.HTTP_200_OK)


class SubmitTestView(APIView):
    """
    Завершение теста и подсчет количества правильных ответов.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, test_id: int):
        test = get_object_or_404(Test, id=test_id)
        questions = test.questions.all()
        correct = 0

        for question in questions:
            try:
                user_answer = UserAnswer.objects.get(user=request.user, question=question)
                user_answer.completed = True
                user_answer.save()

                if sorted(map(str, user_answer.answer)) == sorted(map(str, question.correct_answers)):
                    correct += 1
            except UserAnswer.DoesNotExist:
                continue

        return Response({
            'correct': correct,
            'total': questions.count()
        }, status=status.HTTP_200_OK)