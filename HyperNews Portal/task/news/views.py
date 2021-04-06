from django.views import View
from django.shortcuts import render, redirect
from json import load
from django.conf import settings
from datetime import datetime

with open(settings.NEWS_JSON_PATH, 'r') as f:
    posts = load(f)

class CreateNews(View):
    def get(self, request):
        return render(request, "news/create_news.html")

    def post(self, request):
        created = datetime.now()
        posts.append({"created": created.strftime("%d/%m/%Y %H:%M:%S"),
                      "title": request.POST.get("title"),
                      "text": request.POST.get("text"),
                      "link": created.strftime("d%m%Y%H%M%S")})
        return redirect("/news/")

class NewsView(View):
    def get(self, request):
        if request.GET.get("q"):
            searched_posts = [post for post in posts if request.GET.get("q").lower() in post["title"].lower()]
            context = {
                "articles": searched_posts
            }
        else:
            context = {
            "articles": posts
            }
        return render(request, "news/all_news.html", context)

class PostView(View):
    def get(self, request, link):
        post = next(post for post in posts if post["link"] == link)
        return render(request, "news/news.html", context=post)

class MainIndexView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")