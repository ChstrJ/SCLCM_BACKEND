from django.urls import path, include
from . views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('routine_interview', RoutineInterviewViewset, basename='routine_interview')
router.register('individual_record_form', IndividualRecordFormViewset, basename='individual_record_form')
router.register('careertracking', CareerTrackingViewset, basename='careertracking')
router.register('conferenceform', ConferenceFormViewset, basename='conferenceform')
router.register('ms_impactevaluation', MS_ImpactEvaluationViewset, basename='ms_impactevaluation')
router.register('ms_counselingserviceevaluation', MS_CounselingServiceEvaluationViewset, basename='ms_counselingserviceevaluation')
router.register('guidance_class_evaluation', Guidance_Class_EvaluationViewset, basename='counseling_service_evaluation')
router.register('kinder', KinderViewset, basename='kinder')
router.register('grade_one', Grade_OneViewset, basename='grade_one')
router.register('grade_two', Grade_TwoViewset, basename='grade_two')
router.register('grade_three', Grade_ThreeViewset, basename='grade_three')
router.register('grade_four', Grade_FourViewset, basename='grade_four')
router.register('grade_five', Grade_FiveViewset, basename='grade_five')
router.register('grade_six', Grade_SixViewset, basename='grade_six')
router.register('grade_seven', Grade_SevenViewset, basename='grade_seven')
router.register('grade_eight', Grade_EightViewset, basename='grade_eight')  
router.register('grade_nine', Grade_NineViewset, basename='grade_nine')
router.register('grade_ten', Grade_TenViewset, basename='grade_ten')
router.register('grade_eleven', Grade_ElevenViewset, basename='grade_eleven')
router.register('grade_twelve', Grade_TwelveViewset, basename='grade_twelve')
router.register('first_year', First_YearViewset, basename='first_year')
router.register('second_year', Second_YearViewset, basename='second_year')
router.register('third_year', Third_YearViewset, basename='third_year')
router.register('fourth_year', Fourth_YearViewset, basename='fourth_year')
router.register('resource', ResourceViewSet, basename='resource')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('api/appointment/', AppointmentView.as_view(), name='appointment'),
    path('api/appointment/<int:pk>/', AppointmentView.as_view(), name='appointment-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('api/familyproblem_analytics/', Family_Problem_Analytics.as_view(), name='familyproblem_analytics'),
    path('api/friendsproblem_analytics/', Friends_Problem_Analytics.as_view(), name='friendsproblem_analytics'),
    path('api/healthproblem_analytics/', Health_Problem_Analytics.as_view(), name='healthproblem_analytics'),
    path('api/academicproblem_analytics/', Academic_Problem_Analytics.as_view(), name='academicproblem_analytics'),
    path('api/careerproblem_analytics/', Career_Problem_Analytics.as_view(), name='careerproblem_analytics'),
]
