from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContentCoinDesk

# Create your views here.
from userdashboard.views import isUserSubscribedByRequest, printUserSubscriptionHasRunOut, member

@login_required
def DetailsCoinDesk(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(ContentCoinDesk, pk=pk)
    PageRefAddContent = 'NewBlockchainNews'
    response = render(request, 'user_area/user/Content_Pages/News-Article.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response
