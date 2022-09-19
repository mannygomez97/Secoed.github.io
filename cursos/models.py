from django.db import models
from modelBase.models import ModelBase

class CoursesMoodle(ModelBase):
    moodleId = models.IntegerField(db_column='moodle_id')
    fullname = models.TextField(blank=True, null=True)
    shortname = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
     
    def __str__(self):
        return self.fullname