from django.shortcuts import render, redirect
from dexterapp.views.base_view import BaseView
from dexterapp.service.tag import service as TagService


class PeopleByTagView(BaseView):
    def get(self, request):
        tag_ids = request.GET.get("tag_ids")
        tags = []
        person_tags = []
        if tag_ids:
            tag_ids_list = tag_ids.split(",")
            tags = TagService.get_tags_in_list(request.user,
                                               tag_ids=tag_ids_list)
            person_tags = TagService.get_people_with_tags(user=request.user,
                                                          tag_ids=tag_ids_list)

        context = {
            "tags": tags,
            "person_tags": person_tags
        }

        return render(request, "search/index.html", context)
