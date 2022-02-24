from rest_framework import serializers
from .models import valoration_course_student

class ValCourseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = valoration_course_student
        fields = '__all__'