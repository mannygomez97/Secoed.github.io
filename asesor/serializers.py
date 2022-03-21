from rest_framework import serializers
from .models import valoration_course_student, valoration_module_student_activities

class ValCourseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = valoration_course_student
        fields = '__all__'

class ValModuleStudentActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = valoration_module_student_activities
        fields = '__all__'