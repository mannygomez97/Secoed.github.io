from django.urls import path
from asesor import views

urlpatterns = [
    path('courses_list', views.coursesSecoedView, name='courses_list'),
    path('inactive_courses', views.inactiveCourses, name='inactive_courses'),
    path('listado_estudiante/<id>/<fullname>/', views.listadoEstudiante, name='listado_estudiante'),
    path('actividades_user/<id>/<nombre>/<idest>/', views.userActivities, name='actividades_user'),

    path('modules_by_course/<id>/<fullname>/', views.modulesByCourse, name='modules_by_course'),
    path('details_module/<int:course>/<id>/<fullname>/<name>/<int:section>/', views.detailsModule, name='details_module'),

    path('form_add_schedule_event/<int:courseid>/<fullname>/', views.formAddScheduleEvent, name='form_add_schedule_event'),
    path('save_event_schedule', views.saveScheduleEvent, name='save_event_schedule'),
    path('study_schedule_events/<int:id>/<fullname>/', views.studyScheduleEvents, name='study_schedule_events'),
    path('del_schedule_event/<int:courseid>/<int:id>/<repeatid>/<fullname>/', views.delScheduleEvent, name='del_schedule_event'),

    path('create_module/<int:course>/<int:section>/', views.createModule, name='create_module'),
    path('valoration_course_by_user/<int:courseid>/<userfullname>/<int:userid>/<fullname>/', views.valorationCourseByUser, name='valoration_course_by_user'),
    path('val_module_course/<int:course>/<int:id>/', views.valModuleCourse, name='val_module_course'),
    path('save_val_course/<int:course>/<fullname>/<int:userid>/<name_user>/<napproved>/<activitynumb>/<int:asesor>/<courseMoodle>/', views.saveValCourse, name='save_val_course'),
    path('val_activities_module_users/<int:course>/<int:moduleid>/<fullname>/<namemod>/<int:id>/<name>/', views.valActivitiesModuleUsers, name='val_activities_module_users'),
    
    path('course_notes', views.courseNotes, name='course_notes'),
    path('course_notes_activities', views.activitiesNotes, name='course_notes_activities'),
    path('reports_asesor', views.reportsAsesor, name='reports_asesor'),

    path('tomail/<course_name>/<int:student_id>/<student_name>/<activities_course>/<score_course>/', views.toMail, name='tomail'),
    path('send_mail', views.sendMail, name='send_mail'),

    path('courseInfo/<int:course>', views.valorateCourse, name='courseInfo'),
]