from django.urls import path


from . import views
app_name = 'uploads'
urlpatterns = [
        path('', views.mydrive),
        path('mydrive/', views.mydrive, name='mydrive'),
        path('mydrivetest/', views.mydrivetest, name='mydrivetest'),
        path('folderupload/', views.files_upload, name='folderupload'),
        path('subfolderupload/', views.sub_files_upload, name='subfolderupload'),
        path('upload_driver/',views.upload_driver, name='upload_driver'),
        path('sub_upload_driver/',views.sub_upload_driver, name='sub_upload_driver'),
        path('mydrivetable/', views.mydrivetable, name='mydrivetable'),
        path('mydrivestartable/', views.mydrivestartable, name='mydrivestartable'),
        path('mydrivetrashtable/', views.mydrivetrashtable, name='mydrivetrashtable'),
        path('starred/', views.allStarred, name='allStarred'),
        path('recent/', views.recent, name='recent'),
]

