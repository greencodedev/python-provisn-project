from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.
from userdashboard.views import isUserSubscribedByRequest, printUserSubscriptionHasRunOut, member


@login_required
def DetailsMoiseievYurii(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_Moiseiev_Yurii, pk=pk)
    PageRefAddContent = 'Technical Analysis'
    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required
def DetailsFaibik(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_Faibik, pk=pk)
    PageRefAddContent = 'Technical Analysis'
    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required
def DetailsKhaledAbdulaziz(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_KhaledAbdulaziz, pk=pk)
    PageRefAddContent = 'Technical Analysis'
    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required
def DetailsHamadaMark(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_HamadaMark, pk=pk)
    PageRefAddContent = 'Technical Analysis'
    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required
def DetailsArShevelev(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_ArShevelev, pk=pk)
    PageRefAddContent = 'Technical Analysis'
    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response
