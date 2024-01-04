from django.http import HttpResponseRedirect,HttpResponse
from .models import Question,Choice,uservote
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(question)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        user = User.objects.get(pk=request.user.pk)
        print(user)
        print(selected_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        user_choice = uservote(user=user, choice_text=selected_choice)
        user_choice.save()
        selected_choice.votes+= 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #print(question)
    return render(request, "polls/results.html", {"question": question})


@login_required
def home(request):
    user=request.user.username
    return render(request,'polls/home.html',{'username':user})
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password1')  
            user=authenticate(username=username,password=password)
            login(request,user)
            print(username,password)
            messages.success(request,"Your account is Created Successfully")
            return redirect('home')
        else:
            form=UserCreationForm()
            messages.error(request,"username and password are invalid,Please Try again")
            return render(request,'polls/register.html',{'form':form})     
    else:
        form=UserCreationForm()
        return render(request,'polls/register.html',{'form':form})
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'you have loggedin success')
            print(username,password)
            return redirect('home')
        else:
            messages.success(request, 'username and password are invalid,Please Try again')
            return render(request,'polls/signin.html')    
    else:
        return render(request,'polls/signin.html')
def signout(request):
    logout(request)
    return redirect('signin')



    
    

    