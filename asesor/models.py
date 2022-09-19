from datetime import timedelta
from django.db import models
from conf.models import Carrera
from cursos.models import CoursesMoodle
from eva.models import Ciclo2
from modelBase.models import ModelBase
from components.models import CourseCicleCarrer

class ValorationsCourses(ModelBase):
    courseCicleCarrer = models.ForeignKey(CourseCicleCarrer, on_delete=models.PROTECT,null=False, blank=False)
    course = models.ForeignKey(CoursesMoodle, on_delete=models.PROTECT,null=False, blank=False)
    cicle = models.ForeignKey(Ciclo2, on_delete=models.PROTECT,null=False, blank=False)
    carrer = models.ForeignKey(Carrera, on_delete=models.PROTECT,null=False, blank=False)
    studentId = models.IntegerField(null=False, blank=False)
    studentName = models.CharField(max_length=200, null=True, blank=True)
    activitiesCourse = models.IntegerField(null=False, blank=False, default=0)
    scoreCourse = models.FloatField(null=False, blank=False,)

    def __str__(self):
        return self.course.name + " " + self.studentName + " " + str(self.scoreCourse) 