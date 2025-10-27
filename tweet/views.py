from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


# Home page
def index(request):
    return render(request, 'index.html')

# List all tweets
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-create_on')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Create a new tweet
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

# Edit an existing tweet
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

# Delete a tweet
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        messages.success(request, 'Your Tweet Was Successfully Deleted!' )
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            username = form.cleaned_data.get('username')
            user.save()
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('login')  # redirect to login page after signup
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})