from django.urls import path
from . import views

urlpatterns = [
    # Création d'annonces
    path('creer-annonce/', views.create_annonce, name='creer-annonce'),
    path('login-annonce/', views.login_user, name='login-annonce'),
    path('logout-annonce/', views.logout_annonce, name='logout-annonce'),
    path('logged-annonce/', views.logged_annonce, name='logged-annonce'),

    # Dashboard
    path('dashboard/list/', views.dashboard_list, name='dashboard-list'),
    path('dashboard/<int:pk>/', views.dashboard_view, name='dashboard-annonce'),
    path('dashboard/description/<int:pk>/', views.description_view, name='dashboard-description'),
    path('dashboard/equipment/<int:pk>/', views.equipment_view, name='dashboard-equipment'),
    path('dashboard/duree/<int:pk>/', views.dureeLocation_view, name='dashboard-duree'),
    path('dashboard/loyer/<int:pk>/', views.loyer_view, name='dashboard-loyer'),
    path('dashboard/images/<int:pk>/', views.image_view, name='dashboard-image'),
    path('dashboard/calendrier/<int:pk>/', views.calendrier, name='dashboard-calendrier'),
    path('dashboard/conditions/<int:pk>/', views.condition_view, name='dashboard-conditions'),
    path('dashboard/diagnostic/<int:pk>/', views.diagnsotic_view, name='dashboard-diagnostic'),
    path('dashboard/user/<int:pk>/', views.user_view_dashboard, name='dashboard-user'),
    path('dashboard/verification/<int:pk>/', views.verification_view, name='dashboard-verification'),
    path('dashboard/usercoord/<int:pk>/', views.user_coord_dashboard, name='dashboard-usercoord'),

    # Calendrier
    path('calendrier/create/<int:pk>/', views.create_calendrier, name='create-calendrier'),
    path('calendrier/edit/<int:pk>/', views.edit_calendrier, name='edit-calendrier'),
    path('calendrier/delete/<int:pk>/', views.delete_calendrier, name='delete-calendrier'),
    path('calendrier/delete-confirm/<int:pk>/', views.delete_calendrier_confirm, name='delete-calendrier-confirm'),

    # Images
    path('image/delete/<int:pk>/', views.delete_image, name='delete-image'),

    # Annonces publiques
    path('detail/<int:pk>/', views.detail_annonce, name='detail-annonce'),
    path('gerer-annonce/', views.gerer_annonce, name='gerer-annonce'),
    path('detail_annonce/<str:pk>/', views.detail_annonce, name='detail-annonce'),
    path('selectionner-annonce/<int:pk>/', views.selectionner_annonce, name='selectionner-annonce'),
    path('annuler-selection-annonce/<int:pk>/', views.annuler_selection_annonce, name='annuler-selection-annonce'),
    path('annuler-selection/<int:pk>/', views.annuler_selection_annonce, name='annuler-selection-annonce'),
    path('ajouter-tableau-bord/<int:pk>/', views.ajouter_au_tableau_de_bord, name='ajouter-au-tableau-de-bord'),

    # URLs pour le paiement de caution en mensualités
    path('creer-plan-caution/<int:pk>/', views.creer_plan_paiement_caution, name='creer-plan-caution'),
    path('voir-plan-caution/<int:pk>/', views.voir_plan_paiement_caution, name='voir_plan_paiement_caution'),
    path('effectuer-paiement/<int:pk>/', views.effectuer_paiement_mensuel, name='effectuer_paiement_mensuel'),
    path('plans-caution-proprietaire/', views.liste_plans_paiement_proprietaire, name='liste_plans_paiement_proprietaire'),

    # Profile
    path('profile/', views.profile_annonce, name='profile-annonce'),

    # DocuSign
    path('get-access-code/', views.get_access_code, name='get_access_code'),
    path('auth-login/', views.auth_login, name='auth_login'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),
    path('inscription-simple/', views.inscription_simple, name='inscription-simple'),
]