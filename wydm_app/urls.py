from django.urls import path
from .views import index, form_page, create_invite, view_invite, response_page, spotify_auth, auth_view, spotify_callback, toptracks, generate_recap_image, about, privacy, creator

handler404 = 'wydm_app.views.custom_404'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('privacy/', privacy, name='privacy'),
    path('creator/', creator, name='creator'),
    path('form/<str:option>/', form_page, name='form_page'), # /form/wydm/
    path('wydm/', create_invite, name='wydm'),
    path('wydm/<slug:slug>/', view_invite, name='date'),
    path('wydm/<slug:slug>/response/', response_page, name='response'),
    path('spotify_auth/', spotify_auth, name='spotify_auth'),
    path('callback/', spotify_callback, name='spotify_callback'),
    path('auth/toptracks/', toptracks, name='toptracks'),
    path('generate_recap/', generate_recap_image, name='generate_recap'),

    path('auth/', auth_view, name='auth'),
]
