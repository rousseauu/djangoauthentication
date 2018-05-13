from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from home.forms import HomeForm, ContactForm
from home.models import Post, Friend


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        form = HomeForm()

        posts = Post.objects.all().order_by('-created')

        users = User.objects.exclude(id=request.user.id)
        '''
            Post.objects.all()[1].post get 2nd post
            post =Post.objects.all()
            post.get_next_by_created().post get next post of 2nd post
            post.get_previous_by_created().post get next post of 2nd post
            
        '''

        # friend = Friend.objects.get(users=request.user)
        friend = Friend.objects.get(current_user=request.user)
        # friends = friend.users.exclude(id=request.user.id)
        friends = friend.users.all()
        context = {'form': form, 'posts': posts, 'users': users, 'friends': friends}
        return render(request, self.template_name, context)

    def post(self, request):
        form = HomeForm(request.POST)

        if form.is_valid():
            ''' start model form portion '''
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            ''' end model form portion '''
            # text = form.cleaned_data['post']
            return redirect('home:home')

        context = {'form': form, 'text': text}

        return render(request, self.template_name, context)


class ContactView(TemplateView):
    template_name = 'home/contact.html'

    def get(self, request):
        form = ContactForm()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            pass

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:home')
