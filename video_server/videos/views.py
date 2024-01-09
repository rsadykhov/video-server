from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from videos import models
from users.models import InterfaceCustomization
from django.core.paginator import Paginator



# Utility functions (not views)



def interface_config():
    try:
        interface_customization = InterfaceCustomization.objects.filter(active=True)[0]
        interface_title = interface_customization.title
        hide_videos = interface_customization.hide_videos
    except:
        interface_title = "Home Page"
        hide_videos = False
    return {"interface_title":interface_title, "hide_videos":hide_videos}



def get_page_obj(request, query_set, items_per_page):
    paginator = Paginator(query_set, items_per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)



# Main website


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    # Load main settings
    config_dict = interface_config()
    videos = models.Videos.objects.all().order_by("-uploaded_on")
    # Hide videos with add_to_hidden option
    if config_dict["hide_videos"]:
        videos = videos.filter(add_to_hidden=False)
    # Iterative paginator
    page_obj = get_page_obj(request=request, query_set=videos, items_per_page=12)
    return render(request, "index.html", {"interface_title":config_dict["interface_title"], "title":"Content Library", "page_obj":page_obj})



class UserLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("videos:index")
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))



@user_passes_test(lambda u: u.is_superuser)
def logout_view(request):
    logout(request)
    return redirect("videos:login")



# Content



class VideosDetailView(DetailView, LoginRequiredMixin):
    model = models.Videos
    template_name = "videos_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["interface_title"] = interface_config()["interface_title"]
        video = get_object_or_404(models.Videos, pk=self.kwargs["pk"])
        context["video"] = video
        return context



@user_passes_test(lambda u: u.is_superuser)
def tags_list_view(request):
    interface_title = interface_config()["interface_title"]
    tags_list = models.Tags.objects.all().order_by("n_items")
    page_obj = get_page_obj(request=request, query_set=tags_list, items_per_page=100)
    return render(request, "item_list.html", {"interface_title":interface_title, "title":"Tags", "page_obj":page_obj})



@user_passes_test(lambda u: u.is_superuser)
def tags_detail_view(request, pk):
    # Load main settings
    config_dict = interface_config()
    tag_name = models.Tags.objects.filter(pk=pk)[0].name
    videos = models.Videos.objects.filter(tags__pk=pk).order_by("-uploaded_on")
    # Hide videos with add_to_hidden option
    if config_dict["hide_videos"]:
        videos = videos.filter(add_to_hidden=False)
    # Iterative paginator
    page_obj = get_page_obj(request=request, query_set=videos, items_per_page=12)
    return render(request, "index.html", {"interface_title":config_dict["interface_title"], "title":"#{}".format(tag_name), "page_obj":page_obj})



@user_passes_test(lambda u: u.is_superuser)
def categories_list_view(request):
    interface_title = interface_config()["interface_title"]
    categories_list = models.Categories.objects.all().order_by("n_items")
    page_obj = get_page_obj(request=request, query_set=categories_list, items_per_page=100)
    return render(request, "item_list.html", {"interface_title":interface_title, "title":"Categories", "page_obj":page_obj})



@user_passes_test(lambda u: u.is_superuser)
def categories_detail_view(request, pk):
    # Load main settings
    config_dict = interface_config()
    category_name = models.Categories.objects.filter(pk=pk)[0].name
    videos = models.Videos.objects.filter(categories__pk=pk).order_by("-uploaded_on")
    # Hide videos with add_to_hidden option
    if config_dict["hide_videos"]:
        videos = videos.filter(add_to_hidden=False)
    # Iterative paginator
    page_obj = get_page_obj(request=request, query_set=videos, items_per_page=12)
    return render(request, "index.html", {"interface_title":config_dict["interface_title"], "title":"{}".format(category_name), "page_obj":page_obj})