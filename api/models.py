from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from datetime import time

# Create your models here.
GRADE_LEVEL = [
    ('Grade 1', 'grade 1'),
    ('Grade 2', 'grade 2'),
    ('Grade 3', 'grade 3'),
    ('Grade 4', 'grade 4'),
    ('Grade 5', 'grade 5'),
    ('Grade 6', 'grade 6'),
    ('Grade 7', 'grade 7'),
    ('Grade 8', 'grade 8'),
    ('Grade 9', 'grade 9'),
    ('Grade 10', 'grade 10'),
    ('Grade 11', 'grade 11'),
    ('Grade 12', 'grade 12'),
    ('1st Year', '1st year'),
    ('2nd Year', '2nd year'),
    ('3rd Year', '3rd year'),
    ('4th Year', '4th year'),
]

class Profile(models.Model):
    USER_ROLE = [
        ('counselor', 'counselor'),
        ('psychometrician', 'psychometrician'),
        ('student', 'student')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=USER_ROLE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.role}'

class IndividualRecordForm(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    sr_code = models.CharField(max_length=100, unique=True, primary_key=True, default=1)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    completeAddress = models.CharField(max_length=500, blank=True, null=True)

    fatherName = models.CharField(max_length=255, blank=True, null=True)
    fatherOccupation = models.CharField(max_length=255, blank=True, null=True)
    fatherContactNumber = models.CharField(max_length=255, blank=True, null=True)
    fatherEmailAddress = models.CharField(max_length=255, blank=True, null=True)

    motherName = models.CharField(max_length=255, blank=True, null=True)
    motherOccupation = models.CharField(max_length=255, blank=True, null=True)
    motherContactNumber = models.CharField(max_length=255, blank=True, null=True)
    motherEmailAddress = models.CharField(max_length=255, blank=True, null=True)

    parents = models.JSONField(default=list)

    living_with = models.JSONField(default=list)
    relationship = models.CharField(max_length=255, blank=True, null=True)

    club = models.CharField(max_length=500, blank=True, null=True)

class RoutineInterview(models.Model):
    sr_code = models.ForeignKey(IndividualRecordForm, on_delete=models.SET_NULL, related_name='routine_interview', null=True)
    name = models.CharField(max_length=255)
    section = models.CharField(max_length=100)
    grade = models.CharField(max_length=100, choices=GRADE_LEVEL)
    date = models.DateField()

    family_problem = models.JSONField(default=list, blank=True, null=True)
    family_details = models.TextField(blank=True, null=True)
    friends_problem = models.JSONField(default=list, blank=True, null=True)
    friends_details = models.TextField(blank=True, null=True)
    health_problem = models.JSONField(default=list, blank=True, null=True)
    health_details = models.TextField(blank=True, null=True)
    
    academic_problem = models.JSONField(default=list, blank=True, null=True)
    academic_details = models.TextField(blank=True, null=True)

    career_problem = models.JSONField(default=list, blank=True, null=True)
    career_details = models.TextField(blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)
    recommendation = models.JSONField(default=list, blank=True, null=True)
    other_recommendation = models.CharField(max_length=255, blank=True, null=True)

class CareerTracking(models.Model): 
    name = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    
    cle = models.IntegerField()
    english = models.IntegerField()
    filipino = models.IntegerField()
    ap = models.IntegerField()
    science = models.IntegerField()
    math = models.IntegerField()
    mapeh = models.IntegerField()
    tle = models.IntegerField()
    computer = models.IntegerField()
    fl = models.IntegerField()

    academic_track = models.JSONField(default=list, blank=True, null=True)
    other_track = models.CharField(max_length=255, blank=True, null=True)
    tech_voc = models.JSONField(default=list, blank=True, null=True)
    other_techvoc = models.CharField(max_length=255, blank=True, null=True)
    preferredCourse = models.CharField(max_length=255, blank=True, null=True)

    medical_records = models.JSONField(default=list)
    specify = models.CharField(max_length=255, blank=True, null=True)
    academic_status = models.JSONField(default=list)
    psych_results = models.CharField(max_length=255)

    top_one = models.CharField(max_length=100, blank=True, null=True)
    top_two = models.CharField(max_length=100, blank=True, null=True)
    top_three = models.CharField(max_length=100, blank=True, null=True)

class ConferenceForm(models.Model):
    type = models.JSONField(default=list, blank=True, null=True)
    name = models.CharField(max_length=255)
    date = models.DateField()
    grade = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    teachers = models.CharField(max_length=500)
    purpose = models.JSONField(default=list)
    others = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField()
    recommendations = models.TextField()

class MS_ImpactEvaluation(models.Model):
    name = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    gradelevel = models.JSONField(default=list)
    improved = models.JSONField(default=list)
    interests = models.JSONField(default=list)
    work = models.JSONField(default=list)
    ontime = models.JSONField(default=list)
    careerplan = models.JSONField(default=list)
    respectful = models.JSONField(default=list)
    responsible = models.JSONField(default=list)
    studyhabits = models.JSONField(default=list)
    cooperate = models.JSONField(default=list)
    decided = models.JSONField(default=list)
    careergoals = models.JSONField(default=list)
    prioritize = models.JSONField(default=list)
    positive = models.JSONField(default=list)
    cope = models.JSONField(default=list)
    attentive= models.JSONField(default=list)
    selfcontrol = models.JSONField(default=list)
    aware= models.JSONField(default=list)
    helpful = models.TextField()
    meetingneeds = models.JSONField(default=list)
    satisfaction= models.JSONField(default=list)
    unsureno = models.TextField()
    activities = models.TextField()
    recommenations = models.TextField()
    acquainted = models.JSONField(default=list)
    timetosee = models.JSONField(default=list)
    helpfulness = models.JSONField(default=list)
    comfort = models.JSONField(default=list)
     
class MS_CounselingServiceEvaluation(models.Model):
    name = models.CharField(max_length=255)
    gradelevel = models.JSONField(default=list)
    section = models.JSONField(default=list)
    question_one = models.JSONField(default=list)
    question_two = models.JSONField(default=list)
    question_three = models.JSONField(default=list)
    question_four = models.JSONField(default=list)
    question_five = models.JSONField(default=list)
    question_six = models.JSONField(default=list)
    question_seven = models.JSONField(default=list)
    question_eight = models.JSONField(default=list)
    question_nine = models.JSONField(default=list)
    question_10 = models.JSONField(default=list)

class Guidance_Class_Evaluation(models.Model):
    name = models.CharField(max_length=255)
    grade = models.JSONField(default=list)
    section = models.JSONField(default=list)
    question_1 = models.JSONField(default=list)
    question_2 = models.JSONField(default=list)
    question_3 = models.JSONField(default=list)
    question_4 = models.JSONField(default=list)
    question_5 = models.JSONField(default=list)
    question_6 = models.JSONField(default=list)
    question_7 = models.TextField()
    question_8 = models.TextField()
    question_9 = models.TextField()

class Kinder(models.Model):
    name = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    dateofbirth = models.DateField()
    address = models.CharField(max_length=255)
    pregm = models.CharField(max_length=255)
    presgm = models.CharField(max_length=255)
    prefm = models.CharField(max_length=500)
    presfm= models.CharField(max_length=255)
    presh = models.CharField(max_length=255)
    pressh = models.CharField(max_length=255)
    presrl = models.CharField(max_length=255)
    preel = models.CharField(max_length=255)
    presel = models.CharField(max_length=255)
    prec = models.CharField(max_length=255)
    presc = models.CharField(max_length=255)
    prescalesum = models.CharField(max_length=255)
    prestandardscore = models.CharField(max_length=255)
    preverbalint = models.CharField(max_length=255)
    postgm = models.CharField(max_length=255)
    postsgm = models.CharField(max_length=255)
    postfm = models.CharField(max_length=255)
    postsfm = models.CharField(max_length=255)
    postsh = models.CharField(max_length=255)
    postssh = models.CharField(max_length=255)
    postrl = models.CharField(max_length=255)
    postsrl = models.CharField(max_length=255)
    postel = models.CharField(max_length=255)
    postsel = models.CharField(max_length=255)
    postc = models.CharField(max_length=255)
    postsc = models.CharField(max_length=255)
    postscalesum = models.CharField(max_length=255)
    poststandardscore = models.CharField(max_length=255)
    postverbalint = models.CharField(max_length=255)


class Grade_One(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=100)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    test = models.CharField(max_length=255, blank=True, null=True)
    rawscore = models.CharField(max_length=500)
    percentile= models.CharField(max_length=255)
    stanine = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    vocab = models.CharField(max_length=255)
    letter = models.CharField(max_length=255)
    visual = models.CharField(max_length=255)
    auditory = models.CharField(max_length=255)
    comp = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    writing = models.CharField(max_length=255)
    spelling = models.CharField(max_length=255)
    q_vocab = models.CharField(max_length=255)
    q_letter = models.CharField(max_length=255)
    q_visual = models.CharField(max_length=255)
    q_auditory = models.CharField(max_length=255)
    q_comp = models.CharField(max_length=255)
    q_number = models.CharField(max_length=255)
    q_writing = models.CharField(max_length=255)
    q_spelling = models.CharField(max_length=255)


class Grade_Two(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=100)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    totalEQ = models.CharField(max_length=255, blank=True, null=True)
    verbalInterpretation = models.CharField(max_length=500)
    stanine = models.CharField(max_length=255)
    sa = models.CharField(max_length=255)
    mme = models.CharField(max_length=255)
    sm = models.CharField(max_length=255)
    e = models.CharField(max_length=255)
    hr = models.CharField(max_length=255)

class Grade_Three(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    raw_score = models.CharField(max_length=255)
    percentile = models.CharField(max_length=255)
    stanine = models.CharField(max_length=255)
    verbal_interpretation = models.CharField(max_length=255)

class Grade_Four(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255, blank=True, null=True)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    conduct = models.JSONField(default=list)
    self_image = models.JSONField(default=list)
    worry = models.JSONField(default=list)
    neg_perl_rel = models.JSONField(default=list)
    antisocial = models.JSONField(default=list)
    lie = models.JSONField(default=list)
    problem_index = models.JSONField(default=list)
    c = models.CharField(max_length=255)
    si = models.CharField(max_length=255)
    w = models.CharField(max_length=255)
    npr = models.CharField(max_length=255)
    a_s = models.CharField(max_length=255)
    l = models.CharField(max_length=255)
    pi = models.CharField(max_length=255)

class Grade_Five(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    raw_score = models.CharField(max_length=255)
    percentile = models.CharField(max_length=255)
    stanine = models.CharField(max_length=255)
    verbal_interpretation = models.JSONField(default=list)

class Grade_Six(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    raw_score = models.CharField(max_length=255)
    percentile = models.CharField(max_length=255)
    stanine = models.CharField(max_length=255)
    verbal_interpretation = models.JSONField(default=list)

class Grade_Seven(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255, choices=GRADE_LEVEL)
    section = models.JSONField(default=list)
    tot = models.JSONField(default=list)
    beh = models.JSONField(default=list)
    inte = models.JSONField(default=list)
    phy = models.JSONField(default=list)
    fre = models.JSONField(default=list)
    popularity = models.JSONField(default=list)
    hap = models.JSONField(default=list)
    beh_num = models.CharField(max_length=255, blank=True, null=True)
    int_num = models.CharField(max_length=255, blank=True, null=True)
    phy_num = models.CharField(max_length=255, blank=True, null=True)
    fre_num = models.CharField(max_length=250, blank=True, null=True)
    popularity_num = models.CharField(max_length=250, blank=True, null=True)
    hap_num = models.CharField(max_length=250, blank=True, null=True)

class Grade_Eight(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255, blank=True, null=True)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    conduct = models.JSONField(default=list)
    self_image = models.JSONField(default=list)
    worry = models.JSONField(default=list)
    neg_perl_rel = models.JSONField(default=list)
    antisocial = models.JSONField(default=list)
    lie = models.JSONField(default=list)
    problem_index = models.JSONField(default=list)
    c = models.CharField(max_length=255)
    si = models.CharField(max_length=255)
    w = models.CharField(max_length=255)
    npr = models.CharField(max_length=255)
    a_s = models.CharField(max_length=255)
    l = models.CharField(max_length=255)
    pi = models.CharField(max_length=255)

class Grade_Nine(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255, blank=True, null=True)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    top_one = models.JSONField(default=list)
    top_two = models.JSONField(default=list)
    top_three = models.JSONField(default=list)
    self_control = models.JSONField(default=list)
    mas_fem = models.JSONField(default=list)
    status = models.JSONField(default=list)
    infrequency = models.JSONField(default=list)
    acquiescence = models.JSONField(default=list)
    r = models.CharField(max_length=250)
    i = models.CharField(max_length=250)
    a = models.CharField(max_length=250)
    s = models.CharField(max_length=250)
    e = models.CharField(max_length=250)
    c = models.CharField(max_length=250)
    se = models.CharField(max_length=250)
    mf = models.CharField(max_length=250)
    st = models.CharField(max_length=250)
    inf = models.CharField(max_length=250)
    ac = models.CharField(max_length=250)

class Grade_Ten(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    raw_score = models.CharField(max_length=255)
    percentile = models.CharField(max_length=255)
    stanine = models.CharField(max_length=255)
    verbal_interpretation = models.JSONField(default=list)

class Grade_Eleven(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    top_1 = models.CharField(max_length=255)
    top_2 = models.CharField(max_length=255)
    top_3 = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    warmth = models.CharField(max_length=255)
    reasoning= models.CharField(max_length=255)
    emotional= models.CharField(max_length=255, blank=True, null=True)
    dominance = models.CharField(max_length=255)
    liveliness = models.CharField(max_length=255)
    rule_consciousness = models.CharField(max_length=255)
    social_boldness = models.CharField(max_length=255)
    sensitivity = models.CharField(max_length=255)
    vigilance = models.CharField(max_length=255)
    abstract = models.CharField(max_length=255)
    privateness = models.CharField(max_length=255)
    apprehension = models.CharField(max_length=255)
    openness = models.CharField(max_length=255)
    self_reliance = models.CharField(max_length=255)
    perfectionism = models.CharField(max_length=255)
    tension = models.CharField(max_length=255)

class Grade_Twelve(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    section = models.JSONField(default=list)
    top_1 = models.JSONField(default=list)
    top_2 = models.JSONField(default=list)
    top_3 = models.JSONField(default=list)
    ad = models.CharField(max_length=255)
    sc = models.CharField(max_length=255)
    ass = models.CharField(max_length=255)
    so = models.CharField(max_length=255)
    s = models.CharField(max_length=255)
    f = models.CharField(max_length=255)
    c = models.CharField(max_length=255)

class First_Year(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    yearLevel = models.CharField(max_length=255)
    course = models.JSONField(default=list)
    vi_gstm = models.CharField(max_length=255)
    vi_nt = models.CharField(max_length=255)
    vi_epp = models.CharField(max_length=255)
    vi_w = models.CharField(max_length=255)
    vi_mc = models.CharField(max_length=255)
    vi_cuca = models.CharField(max_length=255)
    vi_asm = models.CharField(max_length=255)
    gtsm = models.CharField(max_length=255)
    nt = models.CharField(max_length=255)
    epp = models.CharField(max_length=255)
    w = models.CharField(max_length=255)
    mc = models.CharField(max_length=255)
    cu_ca = models.CharField(max_length=255)
    asm = models.CharField(max_length=255)

class Second_Year(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    course = models.JSONField(default=list)
    inc = models.CharField(max_length=255)
    intrapersonal = models.CharField(max_length=255)
    stress_management = models.CharField(max_length=255)
    adaptability = models.CharField(max_length=255)
    general_mood = models.CharField(max_length=255)
    total_eq = models.CharField(max_length=255)
    positive_impression = models.CharField(max_length=255)
    a_vi= models.CharField(max_length=255)
    b_vi = models.CharField(max_length=255)
    c_vi = models.CharField(max_length=255)
    d_vi = models.CharField(max_length=255)
    e_vi = models.CharField(max_length=255)
    f_vi = models.CharField(max_length=255)
    g_vi = models.CharField(max_length=255)
    
class Third_Year(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    course = models.JSONField(default=list)
    hypochondriasis = models.CharField(max_length=255)
    denial = models.CharField(max_length=255)
    interpersonal_problems = models.CharField(max_length=255)
    alienation = models.CharField(max_length=255)
    persecutory_ideas = models.CharField(max_length=255)
    anxiety = models.CharField(max_length=255)
    thinking_disorder = models.CharField(max_length=255)
    impulse_expression = models.CharField(max_length=255)
    social_isolation = models.CharField(max_length=255)
    self_depreciation = models.CharField(max_length=255)
    deviation = models.CharField(max_length=255)
    
class Fourth_Year(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.JSONField(default=list)
    gradeLevel = models.CharField(max_length=255)
    course_program = models.JSONField(default=list)
    l_raw = models.CharField(max_length=255)
    l_s = models.CharField(max_length=255)
    l_vi = models.CharField(max_length=255)
    q_percent = models.CharField(max_length=255)
    q_s = models.CharField(max_length=255)
    sq_vi = models.CharField(max_length=255)
    t_raw = models.CharField(max_length=255)
    t_percent = models.CharField(max_length=255)
    t_s = models.CharField(max_length=255)
    t_vi = models.CharField(max_length=255)
    kiersey = models.CharField(max_length=255)
    written = models.CharField(max_length=255)
    negotiating_persuading = models.CharField(max_length=255)
    verbal_communication = models.CharField(max_length=255)
    co_op = models.CharField(max_length=255)
    investigating_analyzing = models.CharField(max_length=255)
    leadership = models.CharField(max_length=255)
    planning_organizing = models.CharField(max_length=255)
    numeracy = models.CharField(max_length=255)

class Resource(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), related_name='resource', on_delete=models.CASCADE, default=1)
    attachment = models.FileField(upload_to='resource/', blank=True, null=True)


    def __str__(self) -> str:
        return self.title

class Appointment(models.Model):
    PURPOSE_CHOICES = [
        ('Routine Interview', 'Routine Interview'),
        ('Referral', 'Referral'),
        ('Individual Planning', 'Individual Planning'),
        ('Counseling', 'Counseling'),
        ('Others', 'Others'),
    ]

    sr_code = models.ForeignKey(IndividualRecordForm, on_delete=models.SET_NULL, related_name='appointments', null=True)
    counselor = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='counselor_appointments', null=True)
    name = models.CharField(max_length=255)
    grade = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField(default=time(9, 0))
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    other_purpose = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Counselor: {self.counselor} - Student: {self.name} on {self.date}"


class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name