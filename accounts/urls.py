# accounts/urls.py

from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import customer, seller


urlpatterns = [
    path('customer/', include(([
        path('dashboard/', TemplateView.as_view(
            template_name='dashboard/customer/index.html'), name='customer_dashboard'),
        # path('', customer.QuizListView.as_view(), name='quiz_list'),
        # path('interests/', customer.StudentInterestsView.as_view(), name='student_interests'),
        # path('taken/', customer.TakenQuizListView.as_view(), name='taken_quiz_list'),
        # path('quiz/<int:pk>/', customer.take_quiz, name='take_quiz'),
    ], 'accounts'), namespace='customer')),

    path('seller/', include(([
        path('dashboard/', seller.StoreProfileDetailView.as_view(
            extra_context={'page_description': "Tableau de bord"}), name='profile'),

        path('settings/', seller.StoreUpdateView.as_view(
            extra_context={'page_description': "Configuration"}), name='update'),

        # path('', seller.QuizListView.as_view(), name='quiz_change_list'),
        # path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        # path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        # path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        # path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        # path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'accounts'), namespace='seller')),
]