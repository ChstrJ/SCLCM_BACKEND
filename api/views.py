from email.utils import parsedate
from pathlib import Path
from venv import logger
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets, permissions
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.db import connection, transaction
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models import Count, Q
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import os

# Create your views here.
class StudentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        students = IndividualRecordForm.objects.values("sr_code")  # Adjust field name if necessary
        return Response(list(students))
    
class RegisterView(APIView):
    def post(self, request):
        try:
            # Extract data from request
            username = request.data.get('username')
            password = request.data.get('password')
            role = request.data.get('role')  # Role ('Counselor', 'Psychometrician', 'Student')

            # Log the role received from frontend for debugging
            print(f"Backend received role: {role}")  # Ensure this prints the correct role

            # Validate role (case insensitive check)
            valid_roles = ['counselor', 'psychometrician', 'student']
            if role.lower() not in valid_roles:
                return Response({'message': 'Invalid role specified'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user_data = {'username': username, 'password': password}
            serializer = RegistrationSerializer(data=user_data)

            if serializer.is_valid():
                # Save user after validation
                user = serializer.save()

                # Create profile and assign the role directly here
                print(f"Creating profile with role: {role.lower()}")
                Profile.objects.create(user=user, role=role.lower())  # Role should be saved in lowercase

                return Response({
                    'message': 'User created successfully',
                    'username': user.username,
                    'role': role,
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Error occurred:", str(e))  # This will print any error to the console
            return Response({'message': 'Internal Server Error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class setPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BaseViewSet(viewsets.ModelViewSet):

    def close_connection(self):
        """Close any existing database connections to avoid stale data."""
        connection.close()

    @method_decorator(never_cache)
    def list(self, request):
        self.close_connection()
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(never_cache)
    def create(self, request):
        self.close_connection()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @method_decorator(never_cache)
    def retrieve(self, request, pk=None):
        self.close_connection()
        project = get_object_or_404(self.queryset, pk=pk)
        project.refresh_from_db()
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    @method_decorator(never_cache)
    def update(self, request, pk=None):
        self.close_connection()
        project = get_object_or_404(self.queryset, pk=pk)
        project.refresh_from_db()
        serializer = self.serializer_class(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @method_decorator(never_cache)
    def destroy(self, request, pk=None):
        self.close_connection()
        project = get_object_or_404(self.queryset, pk=pk)
        project.refresh_from_db()
        project.delete()
        return Response(status=204)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            # User is authenticated, return token and role
            token, created = Token.objects.get_or_create(user=user)
            user_role = user.profile.role  # Assuming you have a `role` field in a `profile` model
            return Response({'token': token.key, 'role': user_role}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
def search_student(request):
    query = request.GET.get('query', '').strip()
    if query:
        students = IndividualRecordForm.objects.filter(
            Q(sr_code__icontains=query) |
            Q(lastname__icontains=query) |
            Q(firstname__icontains=query)
        ).select_related('profile').distinct()

        results = [
            {
                'sr_code': student.sr_code,
                'firstname': student.firstname,
                'lastname': student.lastname,
                'year': student.year,
                'section': student.section
            }
            for student in students
        ]

        return JsonResponse({'results': results}, safe=False)
    return JsonResponse({'results': []}) 
        
class RoutineInterviewViewset(BaseViewSet):
    queryset = RoutineInterview.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RoutineInterviewSerializer
    
class IndividualRecordFormViewset(BaseViewSet):
    queryset = IndividualRecordForm.objects.order_by('-sr_code')
    serializer_class = IndividualRecordFormSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(profile=profile)  # Associate the profile
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the logged-in user."},
                status=status.HTTP_404_NOT_FOUND
            )
    
class CareerTrackingViewset(BaseViewSet):
    queryset = CareerTracking.objects.order_by('-id')
    serializer_class = CareerTrackingSerializer
    permission_classes = [permissions.AllowAny]

class ConferenceFormViewset(BaseViewSet):
    queryset = ConferenceForm.objects.order_by('-id')
    serializer_class = ConferenceFormSerializer
    permission_classes = [permissions.AllowAny]

class MS_ImpactEvaluationViewset(BaseViewSet):
    queryset = MS_ImpactEvaluation.objects.order_by('-id')
    serializer_class = MS_ImpactEvaluationSerializer
    permission_classes = [permissions.AllowAny]

class MS_CounselingServiceEvaluationViewset(BaseViewSet):
    queryset = MS_CounselingServiceEvaluation.objects.order_by('-id')
    serializer_class = MS_CounselingServiceEvaluationSerializer
    permission_classes = [permissions.AllowAny]

class Guidance_Class_EvaluationViewset(BaseViewSet):
    queryset = Guidance_Class_Evaluation.objects.order_by('-id')
    serializer_class = Guidance_Class_EvaluationSerializer
    permission_classes = [permissions.AllowAny]

class KinderViewset(BaseViewSet):
    queryset = Kinder.objects.order_by('-id')
    serializer_class = KinderSerializer  


class Grade_OneViewset(BaseViewSet):
    queryset = Grade_One.objects.order_by('-id')
    serializer_class = Grade_OneSerializer  

class Grade_TwoViewset(BaseViewSet):
    queryset = Grade_Two.objects.order_by('-id')
    serializer_class = Grade_TwoSerializer  
    permission_classes = [permissions.AllowAny]
    
class Grade_ThreeViewset(BaseViewSet):
    queryset = Grade_Three.objects.order_by('-id')
    serializer_class = Grade_ThreeSerializer
    permission_classes = [permissions.AllowAny]

class Grade_FourViewset(BaseViewSet):
    queryset = Grade_Four.objects.order_by('-id')
    serializer_class = Grade_FourSerializer
    permission_classes = [permissions.AllowAny]

class Grade_FiveViewset(BaseViewSet):
    queryset = Grade_Five.objects.order_by('-id')
    serializer_class = Grade_FiveSerializer
    permission_classes = [permissions.AllowAny]

class Grade_SixViewset(BaseViewSet):
    queryset = Grade_Six.objects.order_by('-id')
    serializer_class = Grade_SixSerializer
    permission_classes = [permissions.AllowAny]

class Grade_SevenViewset(BaseViewSet):
    queryset = Grade_Seven.objects.order_by('-id')
    serializer_class = Grade_SevenSerializer
    permission_classes = [permissions.AllowAny]

class Grade_EightViewset(BaseViewSet):
    queryset = Grade_Eight.objects.order_by('-id')
    serializer_class = Grade_EightSerializer
    permission_classes = [permissions.AllowAny]

class Grade_NineViewset(BaseViewSet):
    queryset = Grade_Nine.objects.order_by('-id')
    serializer_class = Grade_NineSerializer
    permission_classes = [permissions.AllowAny]

class Grade_TenViewset(BaseViewSet):
    queryset = Grade_Ten.objects.order_by('-id')
    serializer_class = Grade_TenSerializer
    permission_classes = [permissions.AllowAny]

class Grade_ElevenViewset(BaseViewSet):
    queryset = Grade_Eleven.objects.order_by('-id')
    serializer_class = Grade_ElevenSerializer

class Grade_TwelveViewset(BaseViewSet):
    queryset = Grade_Twelve.objects.order_by('-id')
    serializer_class = Grade_TwelveSerializer

class First_YearViewset(BaseViewSet):
    queryset = First_Year.objects.order_by('-id')
    serializer_class = First_YearSerializer

class Second_YearViewset(BaseViewSet):
    queryset = Second_Year.objects.order_by('-id')
    serializer_class = Second_YearSerializer

class Third_YearViewset(BaseViewSet):
    queryset = Third_Year.objects.order_by('-id')
    serializer_class = Third_YearSerializer

class Fourth_YearViewset(BaseViewSet):
    queryset = Fourth_Year.objects.order_by('-id')
    serializer_class = Fourth_YearSerializer

class ProjectViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.order_by('-id')
    serializer_class = ProjectSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)

    def retrieve(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)

    def destroy(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        project.delete()
        return Response(status=204)
    
class ResourceViewSet(BaseViewSet):
    queryset = Resource.objects.order_by('-created', '-modified')
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    resource = serializer.save(author=request.user)  # Automatically set the author to the logged-in user
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"An error occurred: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AppointmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        
        if user_profile.role == 'student':
            appointments = Appointment.objects.filter(sr_code__profile=user_profile)
        else:
            appointments = Appointment.objects.all()
        
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Ensure sr_code is a valid instance of IndividualRecordForm
        try:
            student = IndividualRecordForm.objects.get(sr_code=request.data.get('sr_code'))
        except IndividualRecordForm.DoesNotExist:
            return Response({'error': 'Invalid sr_code. No student found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Automatically assign the counselor field from the logged-in user (who is creating the appointment)
        user_profile = Profile.objects.get(user=request.user)
        
        # Add counselor to the request data
        request.data['counselor'] = user_profile.id  # Add the logged-in counselor's ID

        # Serialize the data
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            # Fetch the appointment by primary key (ID)
            appointment = Appointment.objects.get(pk=pk)
            
            # Authorization: Allow deletion only by the counselor who created it or an admin
            if request.user.profile.role != 'admin' and appointment.counselor.user != request.user:
                return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Delete the appointment
            appointment.delete()
            return Response({'message': 'Appointment deleted successfully.'}, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class Family_Problem_Analytics(APIView):
    def get(self, request):
        grade = request.query_params.get('grade', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = RoutineInterview.objects.all()

        if grade:
            queryset = queryset.filter(grade=grade)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        stats = queryset.values('family_problem').annotate(count=Count('family_problem'))
        return Response(stats)
    
class Friends_Problem_Analytics(APIView):
    def get(self, request):
        grade = request.query_params.get('grade', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = RoutineInterview.objects.all()

        if grade:
            queryset = queryset.filter(grade=grade)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
            
            stats = queryset.values('friends_problem').annotate(count=Count('friends_problem'))
            return Response(stats)

class Health_Problem_Analytics(APIView):
    def get(self, request):
        grade = request.query_params.get('grade', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = RoutineInterview.objects.all()

        if grade:
            queryset = queryset.filter(grade=grade)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
            
            stats = queryset.values('health_problem').annotate(count=Count('health_problem'))
            return Response(stats)
    
class Academic_Problem_Analytics(APIView):
    def get(self, request):
        grade = request.query_params.get('grade', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = RoutineInterview.objects.all()

        if grade:
            queryset = queryset.filter(grade=grade)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
            
            stats = queryset.values('academic_problem').annotate(count=Count('academic_problem'))
            return Response(stats)
    
class Career_Problem_Analytics(APIView):
   def get(self, request):
        grade = request.query_params.get('grade', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = RoutineInterview.objects.all()

        if grade:
            queryset = queryset.filter(grade=grade)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
            
            stats = queryset.values('career_problem').annotate(count=Count('career_problem'))
            return Response(stats)
    
class RoutineInterview_Analytics(APIView):
    def get(self, request):
        # Get query parameters for time filtering
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Base queryset
        queryset = RoutineInterview.objects.all()
                            
        # Apply date filtering if parameters are provided
        if start_date:
            queryset = queryset.filter(created_at__gte=parsedate(start_date))
        if end_date:
            queryset = queryset.filter(created_at__lte=parsedate(end_date))

        # Count non-null entries for each problem field
        family_problem_count = queryset.filter(family_problem__isnull=False).count()
        friends_problem_count = queryset.filter(friends_problem__isnull=False).count()
        health_problem_count = queryset.filter(health_problem__isnull=False).count()
        academic_problem_count = queryset.filter(academic_problem__isnull=False).count()
        career_problem_count = queryset.filter(career_problem__isnull=False).count()

        # Return the counts as a response
        return Response({
            "family_problem_count": family_problem_count,
            "friends_problem_count": friends_problem_count,
            "health_problem_count": health_problem_count,
            "academic_problem_count": academic_problem_count,
            "career_problem_count": career_problem_count
        })

class ProblemTrendAnalysisView(APIView):
    def get(self, request):
        problem_data = {
            "family_problem_counts": [],
            "friends_problem_counts": [],
            "health_problem_counts": [],
            "academic_problem_counts": [],
            "career_problem_counts": [],
        }

        grades = ["Kinder", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "1st Year", "2nd Year", "3rd Year", "4th Year"]

        for grade in grades:
            problems = RoutineInterview.objects.filter(grade=grade)

            problem_data["family_problem_counts"].append(problems.filter(family_problem=True).count())
            problem_data["friends_problem_counts"].append(problems.filter(friends_problem=True).count())
            problem_data["health_problem_counts"].append(problems.filter(health_problem=True).count())
            problem_data["academic_problem_counts"].append(problems.filter(academic_problem=True).count())
            problem_data["career_problem_counts"].append(problems.filter(career_problem=True).count())

        return Response(problem_data)
    
class CareerTrackingView(APIView):
    def get(self, request, student_id):
        try:
            career_tracking = CareerTracking.objects.get(student_id=student_id)
            serializer = CareerTrackingSerializer(career_tracking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CareerTracking.DoesNotExist:
            return Response({"error": "Career tracking not found"}, status=status.HTTP_404_NOT_FOUND)   
        
class FileUploadView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        if 'upload' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        document = request.FILES['upload']
        allowed_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx']

        # Validate file type
        file_extension = os.path.splitext(document.name)[-1].lower().strip('.')
        if file_extension not in allowed_extensions:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        # Save file
        fs = FileSystemStorage()
        filename = fs.save(document.name, document)
        file_url = fs.url(filename)

        return JsonResponse({'url': file_url})


class StorageView(APIView):

    def post(self, request):
        allowed_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']

        file = request.FILES.get('file')

        if not file or not request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        fs = FileSystemStorage()
        file_name = file.name.replace(' ', '_')

        file_extension = Path(file_name).suffix

        if file_extension not in allowed_extensions:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        try:
            fs.save(file_name, file)
        except Exception as e:
            print('Error occurred', e)
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})


class ListFilesView(APIView):
    def get(self, request):

        files = os.listdir(settings.MEDIA_ROOT)
        file_urls = [f"{settings.MEDIA_URL}{file}" for file in files]

        return Response({'files': file_urls})
