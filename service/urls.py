from django.urls import path

from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('paslaugos/', views.paslaugos, name='paslaugos'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas-detail'),
    path('myorders/', views.VartotojoUzsakymuListView.as_view(), name='my-in-progress'),
    path('uzsakymai/naujas', views.VartotojoUzsakymuCreateView.as_view(), name='naujas-manouzsakymas'),
    path('uzsakymai/<int:pk>/redaguoti', views.VartotojoUzsakymuUpdateView.as_view(), name='manouzsakymas-redaguoti'),
    path('uzsakymai/<int:pk>/redaguotiuzsakyma', views.UzsakymoUpdateView.as_view(), name='uzsakymas-redaguoti'),
    path('uzsakymai/<int:pk>/istrinti', views.VartotojoUzsakymuDeleteView.as_view(), name="manouzsakymas-istrinti"),
    path('uzsakymai/<int:pk>/istrintiuzsakyma', views.UzsakymoDeleteView.as_view(), name="uzsakymas-istrinti"),
    path("uzsakymai/<int:pk>/pridetieilute", views.VartotojoEilutesCreateView.as_view(), name="uzsakymai_pridetieilute"),
    path("uzsakymai/<int:uzsakymai_pk>/redaguotieilute/<int:pk>", views.VartotojoEilutesUpdateView.as_view(),
         name="uzsakymai_redaguotieilute"),
    path("uzsakymai/<int:uzsakymai_pk>/istrintieilute/<int:pk>", views.VartotojoEilutesDeleteView.as_view(),
         name="uzsakymai_istrintieilute"),
    path('search/', views.search, name='search'),
    path('logout/', views.CustomLogout.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('i18n/', include('django.conf.urls.i18n')),
]