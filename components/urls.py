from django.urls import path
from components import views
# app_name = "components"
urlpatterns = [
    #Educativo
    # path('obtenerPorcentaje/',views.obtenerPorcentaje, name="obtenerPorcentaje"),

    #Obtiene los asesores filtrados y devuelve en formato JSON
    path('asesor/<str:asesor>',views.asesor, name="obtenerAsesor"),


    path('cursoAsignado/<str:curso>',views.cursoA, name="obtenerCursoA"),

        # Requisito
    path(r'requisito', views.menu, name='requisito'),
    path(r'newRequisito', views.requisito, name='newRequisito'),
    path(r'ajax/loadRequisito', views.loadRequisito, name='loadRequisito'),

    path(r'formrequisito',views.menu, name='forms-requisito'),
    path(r'deleteRequisito/<int:pk>',views.deleteRequisito, name='deleteRequisito'),

    path('updateRequisito/<int:pk>',views.UpdateRequisito.as_view(), name = 'updateRequisito'),



    #Guarda asesor Curso
    path('guardarAsesorCurso', views.guardarAsesorCurso, name = 'guardarAsesor'),
    path('notify/email',views.sendEmail, name='sendEmail'),
    path('notify/pdf',views.getPDF, name='getPDF'),

    #Listado de asesor
    path('listado-Asesor', views.listadoAsesores.as_view(), name = 'listadoAsesores'),

    path('actividades', views.actividades.as_view(), name = 'actividades'),


    # Requisito
    path(r'requisito', views.menu, name='requisito'),
    path(r'newRequisito', views.requisito, name='newRequisito'),
    path(r'ajax/loadRequisito', views.loadRequisito, name='loadRequisito'),
    path(r'editRequisito/<int:pk>', views.editRequisito, name='editRequisito'),
    path(r'formrequisito',views.menu, name='forms-requisito'),

    #UI-ELEMENTS
    path('alerts',views.AlertsView.as_view(),name='uielements-alerts'),
    path('buttons',views.ButtonsView.as_view(),name='uielements-buttons'),
    path('cards',views.CardsView.as_view(),name='uielements-cards'),
    path('carousel',views.CarouselView.as_view(),name='uielements-carousel'),
    path('dropdowns',views.DropDownsView.as_view(),name='uielements-dropdowns'),
    path('grid',views.GridView.as_view(),name='uielements-grid'),
    path('images',views.ImagesView.as_view(),name='uielements-images'),
    path('lightbox',views.LightBoxView.as_view(),name='uielements-lightbox'),
    path('modals',views.ModalsView.as_view(),name='uielements-modals'),
    path('rangeslidebar',views.RangeSlidebarView.as_view(),name='uielements-rangeslidebar'),
    path('sessiontimeout',views.SessionTimeoutView.as_view(),name='uielements-sessiontimeout'),
    path('progressbars',views.ProgressBarsView.as_view(),name='uielements-progressbars'),
    path('sweetalert',views.SweetAlertView.as_view(),name='uielements-sweetalert'),
    path('tabs&accordians',views.TabsView.as_view(),name='uielements-tabs'),
    path('typography',views.TypoGraphyView.as_view(),name='uielements-typography'),
    path('video',views.VideoView.as_view(),name='uielements-video'),
    path('general',views.GeneralView.as_view(),name='uielements-general'),
    path('colors',views.ColorsView.as_view(),name='uielements-colors'),
    path('rating',views.RatingView.as_view(),name='uielements-rating'),
    path('notifications',views.NotificationsView.as_view(),name='uielements-notifications'),

    #FORMS
    path('formelements',views.FormelementsView.as_view(),name='forms-formelements'),
    path('formlayouts',views.FormLayoutsView.as_view(),name='forms-formlayouts'),
    path('formvalidation',views.FormValidationView.as_view(),name='forms-formvalidation'),
    path('formadvanced',views.FormAdvancedView.as_view(),name='forms-formadvanced'),
    path('formeditors',views.FormEditorsView.as_view(),name='forms-formeditors'),
    path('formfileupload',views.FormFileuploadView.as_view(),name='forms-formfileupload'),
    path('formxeditable',views.FormXeditableView.as_view(),name='forms-formxeditable'),
    path('formrepeater',views.FormRepeaterView.as_view(),name='forms-formrepeater'),
    path('formwizard',views.FormWizardView.as_view(),name='forms-formwizard'),
    path('formmask',views.FormMaskView.as_view(),name='forms-formmask'),
    path('formeducativo',views.FormEducacion.as_view(), name='forms-educativo'),
    path('formeducativo1',views.FormEducaciona.as_view(), name='forms-educativo1'),
    path('formevaluation',views.FormEvaluation.as_view(), name='forms-evaluation'),

    # path('formrequisito',views.FormRequisito.as_view(), name='forms-requisito'),

    path('formasesor',views.FormAsesor.as_view(), name="forms-asesor"),

    #Tables
    path('basictables',views.BasicTablesView.as_view(),name='tables-basictables'),
    path('datatables',views.DataTablesView.as_view(),name='tables-datatables'),
    path('responsivetables',views.ResponsiveTablesView.as_view(),name='tables-responsivetables'),
    path('editabletables',views.EditableTablesView.as_view(),name='tables-editabletables'),

    #Charts
    path('apexcharts',views.ApexChartsView.as_view(),name='charts-apexcharts'),
    path('echarts',views.EChartsView.as_view(),name='charts-echarts'),
    path('chartjs',views.ChartJsView.as_view(),name='charts-chartjs'),
    path('flotcharts',views.FlotChartsView.as_view(),name='charts-flotcharts'), 
    path('toastuicharts',views.ToastUiChartsView.as_view(),name='charts-toastuicharts'), 
    path('jqueryknobcharts',views.JqueryKnobChartsView.as_view(),name='charts-jqueryknobcharts'), 
    path('sparklinecharts',views.SparklineChartsView.as_view(),name='charts-sparklinecharts'),

    #Icons
    path('boxicons',views.BoxIconsView.as_view(),name='icons-boxicons'),
    path('materialdesign',views.MaterialDesignView.as_view(),name='icons-materialdesign'),
    path('dripicons',views.DripIconsView.as_view(),name='icons-dripicons'),
    path('fontawesome',views.FontAwesomeView.as_view(),name='icons-fontawesome'),

    #Maps
    path('googlemaps',views.GoogleMapsView.as_view(),name='maps-googlemaps'),
    path('vectormaps',views.VectorMapsView.as_view(),name='maps-vectormaps'),
    path('leafletmaps',views.LeafletMapsView.as_view(),name='maps-leafletmaps'),

]