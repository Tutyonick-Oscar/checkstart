from django.urls import path,include
from rest_framework import routers
from checkstart.apps.student.views.index import StudentsView
from checkstart.apps.student.views.fake import CreateFakeUsersView,CreateFakeStudentView,CreateFakeInvoicesView

app_name = 'student'
router = routers.DefaultRouter()
router.register(r"students",StudentsView,basename='students-api-view')
urlpatterns = [
    path('',include(router.urls)),
    path('create-fake-users/',CreateFakeUsersView.as_view(),name='create-fake-users'),
    path('create-fake-students/',CreateFakeStudentView.as_view(),name='create-fake-students'),
    path('create-fake-invoices/',CreateFakeInvoicesView.as_view(),name='create-fake-invoices')
]