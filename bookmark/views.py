from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView,View
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from bookmark.regiform import RegistrationFrom,BookMarkSaveForm
from bookmark.models import Link, BookMark,Tag
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.    
class BookMarksSavePage(TemplateView):
    template_name = 'bookmark_save.html'
    
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return TemplateView.dispatch(self, request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        form = BookMarkSaveForm(request.POST)
        if form.is_valid():
            link,dummy = Link.objects.get_or_create(url = form.cleaned_data['url'])
            bookmark,created = BookMark.objects.get_or_create(user = request.user,link = link)
            bookmark.title = form.cleaned_data['title']
            if not created:
                bookmark.tag_set.clear()
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag,dummy = Tag.objects.get_or_create(name = tag_name)
                bookmark.tag_set.add(tag)
            bookmark.save()
            return HttpResponseRedirect(reverse('user_book_marks',args=[request.user.username]))
        return render(request,'bookmark_save.html',{'form':form})
            
    def get(self,request,*args,**kwargs):
        self.form = BookMarkSaveForm()
        return super(BookMarksSavePage,self).get(self,request,*args,**kwargs)
    
    def get_context_data(self,**kwargs):
        context = super(BookMarksSavePage,self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
    
class RegisterPage(TemplateView):
    template_name = 'register.html'
    
    def post(self,request,*args,**kwargs):
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['password1'])
            login(request,user)
            return render(request,'main_page.html')
        return render(request,'register.html',{'form':form})
            
    def get(self,request,*args,**kwargs):
        self.form = RegistrationFrom()
        return super(RegisterPage,self).get(self,request,*args,**kwargs)
    
    def get_context_data(self,**kwargs):
        context = super(RegisterPage,self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
    
class HomePage(TemplateView):
    template_name = 'main_page.html'
    
class Logout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home_page'))
    
class UserPage(ListView):
    template_name = 'user_page.html'
    context_object_name = 'book_marks'
    
    def get_queryset(self):
        self.user = User.objects.get(username = self.args[0])
        book_marks = self.user.bookmark_set.all()
        return book_marks
    
    def get_context_data(self,**kwargs):
        context = super(UserPage,self).get_context_data(**kwargs)
        context['user_name'] = self.user
        return context 