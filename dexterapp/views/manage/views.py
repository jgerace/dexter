from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from dexterapp.views.utils import get_url_with_query_params
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)
from dexterapp.views.base_view import BaseView
from dexterapp.service.tag import service as TagService
from dexterapp.service.relationship import service as RelationshipService


class ManageView(BaseView):
    def get(self, request):
        error_message = request.GET.get("error_message")

        tags = TagService.get_tags_for_user(user=request.user)
        relationships = RelationshipService.get_relationships_for_user(user=request.user)

        context = {
            "tags": tags,
            "relationships": relationships,
            "error_message": error_message
        }
        return render(request, "manage/index.html", context)


@login_required
def create_tag(request):
    name = request.POST.get("tag_name")
    user = request.user
    try:
        TagService.create_tag(user=user, name=name)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("manage",
                                                  {"error_message": f"Could not create tag {name}: {e}"}))
    except GenericError as e:
        return redirect(get_url_with_query_params("manage",
                                                  {"error_message": f"Could not create tag {name}"}))

    return redirect("manage")


@login_required
def update_tag(request, tag_id):
    try:
        TagService.update_tag(user=request.user,
                              tag_id=tag_id,
                              name=request.POST.get(f"update_tag_name_{tag_id}"))
    except DoesNotValidate:
        return redirect(get_url_with_query_params("manage",
                                                  {"error_message": f"Tag {tag_id} does not exist"}))

    return redirect("manage")


@login_required
def delete_tag(request, tag_id):
    TagService.delete_tag(user=request.user,
                          tag_id=tag_id)

    return redirect("manage")


@login_required
def create_relationship(request):
    name = request.POST.get("relationship_name")
    user = request.user

    try:
        RelationshipService.create_relationship(user=user,
                                                name=name)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("manage",
                                                  {"error_message": f"Could not create relationship {name}: {e}"}))
    except GenericError as e:
        return redirect(get_url_with_query_params("manage",
                                                  {"error_message": f"Could not create relationship {name}"}))

    return redirect("manage")


@login_required
def update_relationship(request, relationship_id):
    try:
        RelationshipService.update_relationship(user=request.user,
                                                relationship_id=relationship_id,
                                                name=request.POST.get(f"update_relationship_name_{relationship_id}"))
    except DoesNotValidate:
        return redirect(get_url_with_query_params("manage",
                                                  {"error_message": f"Relationship {relationship_id} does not exist"}))

    return redirect("manage")


@login_required
def delete_relationship(request, relationship_id):
    RelationshipService.delete_relationship(user=request.user,
                                            relationship_id=relationship_id)

    return redirect("manage")
