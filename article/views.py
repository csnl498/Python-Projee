from ast import keyword
from email import message
from multiprocessing import context
import re
from turtle import title
from django.shortcuts import render, HttpResponse,redirect,get_object_or_404

import article
from .forms import ArticleForm
from django.contrib import messages
from .models import Article
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="user:login")
def articles(request):
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def detail(request,id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article,id=id)
    return render(request,"detail.html",{"article":article})
    #return HttpResponse("detail:"+str(id))
@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request,"dashboard.html",context)
@login_required(login_url="user:login")
def addArticle(request):
    #form = ArticleForm()
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
       article = form.save(commit =False)
       article.author = request.user
       article.save()
       messages.success(request,"Makale Başarıyla Oluşturuldu.")
       return redirect("article:dashboard")
    return render(request,"addarticle.html",{"form": form}) 
@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance=article)
    if form.is_valid():
        article =  form.save(commit = False)
        article.author = request.user
        article.save()
        message.success(request,"Makale Başarıyla Güncellendi")
        return redirect("article:dashboard")
    return render(request,"update.html",{"form":form})
@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete() #vt den silecek
    messages.success(request,"Makale Başarıyla Silindi")
    return redirect("article:dashboard")
