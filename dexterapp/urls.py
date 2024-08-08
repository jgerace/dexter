from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.user import views as user_views
from .views.manage import views as manage_views
from .views.network import views as network_views
from .views.person import views as person_views
from .views.user.views import HomePageView
from .views.network.views import NetworkProfileView, NetworksView
from .views.person.views import PeopleView, PersonProfileView
from .views.search.views import PeopleByTagView

urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path("profile/", user_views.UserProfileView.as_view(),  name="profile"),

    path("networks/", NetworksView.as_view(), name="networks"),
    path("networks/create/", network_views.create_network, name="create_network"),
    path("networks/<str:network_id>/delete/", network_views.delete_network, name="delete_network"),
    path("networks/<str:network_id>/", NetworkProfileView.as_view(), name="network_profile"),
    path("networks/<str:network_id>/add_person", network_views.add_person, name="add_person_to_network"),
    path("networks/<str:person_id>/add_to_network", network_views.add_person_by_person_id, name="add_person_to_network_by_person_id"),
    path("networks/<str:network_id>/<str:person_id>/delete", network_views.delete_person_by_person_id, name="delete_person_from_network"),

    path("people/", PeopleView.as_view(), name="people"),
    path("people/create/", person_views.create_person, name="create_person"),
    path("people/delete/", person_views.delete_person, name="delete_person"),
    path("people/<str:person_id>/", PersonProfileView.as_view(), name="person_profile"),
    path("people/<str:person_id>/add_email/", person_views.add_email_to_person, name="add_email_to_person"),
    path("people/<str:person_id>/add_phone/", person_views.add_phone_number_to_person, name="add_phone_number_to_person"),
    path("people/<str:person_id>/phones/<str:phone_number_id>/update", person_views.update_phone_number_for_person, name="update_phone_number_for_person"),
    path("people/<str:person_id>/phones/<str:phone_number_id>/delete", person_views.delete_phone_number_for_person, name="delete_phone_number_for_person"),
    path("people/<str:person_id>/emails/<str:email_address_id>/update", person_views.update_email_for_person, name="update_email_for_person"),
    path("people/<str:person_id>/emails/<str:email_address_id>/delete", person_views.delete_email_for_person, name="delete_email_for_person"),
    path("people/<str:person_id>/connections/add", person_views.add_connection_to_person, name="add_connection_to_person"),
    path("people/<str:person_id>/addresses/add", person_views.add_address_to_person, name="add_address_to_person"),
    path("people/<str:person_id>/addresses/<str:address_id>/update", person_views.update_address_for_person, name="update_address_for_person"),
    path("people/<str:person_id>/addresses/<str:address_id>/delete", person_views.delete_address_for_person, name="delete_address_for_person"),
    path("people/<str:person_id>/tags/add", person_views.set_tags_on_person, name="set_tags_on_person"),

    path("manage/", manage_views.ManageView.as_view(), name="manage"),
    path("tags/<str:tag_id>/delete", manage_views.delete_tag, name="delete_tag"),
    path("tags/<str:tag_id>/update", manage_views.update_tag, name="update_tag"),
    path("tags/create/", manage_views.create_tag, name="create_tag"),

    path("relationships/<str:relationship_id>/delete", manage_views.delete_relationship, name="delete_relationship"),
    path("relationships/create/", manage_views.create_relationship, name="create_relationship"),
    path("relationships/<str:relationship_id>/update", manage_views.update_relationship, name="update_relationship"),

    path("people/<str:person_id>/connections/<str:connection_id>/delete", person_views.delete_connection_for_person, name="delete_connection_for_person"),

    path("register/", user_views.RegistrationView.as_view(), name="register"),

    path("search/", PeopleByTagView.as_view(), name="search_by_tag"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
