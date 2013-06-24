
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from login.forms import LoginForm, UtilisateurForm
from login.models import Utilisateur, WatchLater, FavoriteArticle
from django.template import RequestContext

def login(request):
    state = "Please log in below..."
    if ("loggedUserId" in request.session):
        return(HttpResponseRedirect("/home"))
    if request.POST:
        form = LoginForm(request.POST)
        if(form.is_valid()):
            user = authenticate(username = form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                state = 'logged in'
                username = form.cleaned_data["username"]
                loggedUser = User.objects.get(username=username)
                request.session["loggedUserId"] = loggedUser.id
                return(render_to_response("home.html",{"loggedUser": loggedUser}))
    else:
        form = LoginForm()
    context = RequestContext(request,{'message':state, 'form':form})
    return render_to_response('login.html',context)

def home(request):
    loggedUser = getLoggedUserFromRequest(request)
    if (loggedUser):
        return(render_to_response("home.html",{"loggedUser": loggedUser}))
    else:
        return(HttpResponseRedirect("/login"))

def getLoggedUserFromRequest(request):
    if ("loggedUserId" in request.session):
        loggedUserId = request.session["loggedUserId"]
        if (len(User.objects.filter(id=loggedUserId))==1):
            return (User.objects.get(id=loggedUserId))
        else:
            return(None)
    else:
        return(None)

def signin(request):
    if request.GET:
        formUser = SignInForm(request.GET)
        formUtilisateur = UtilisateurForm(request.GET)
        if formUser.is_valid() and formUtilisateur.is_valid():
            user=formUser.save()
            user.set_password(formUser.cleaned_data["password"])
            user.save()
            utilisateur = Utilisateur(profilBase=user, birthday=formUtilisateur.cleaned_data["birthday"])
            utilisateur.save()
            return(HttpResponseRedirect('/login'))
        else:
            return(render_to_response("signin.html",{"formUser":formUser, "formUtilisateur":formUtilisateur}))
    else:
        formUser = SignInForm()
        formUtilisateur = UtilisateurForm()
        context = RequestContext(request,{"formUser":formUser, "formUtilisateur":formUtilisateur})
        return(render_to_response("signin.html",context))


def getFavsFromRequest(request, nbOfArticle):
    return FavoriteArticle.objects.filter(relationUtilisateur=Utilisateur.filter(profilBase=getLoggedUserFromRequest(request))).order_by('-datePubli')[:nbOfArticle]

def getWatchLaterFromRequest(request, mnOfArticle):
    return WatchLater.objects.filter(relationUtilisateur=Utilisateur.filter(profilBase=getLoggedUserFromRequest(request))).order_by('-datePubli')[:nbOfArticle]



