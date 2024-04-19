from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.db.models import Avg, Sum
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q


# Create your views here.
def home(request):
    # query = request.GET.get("title")
    query= None
    allMovies = None
    if 'q' in request.GET :
        query = request.GET.get('q')
        allMovies = Movie.objects.all().filter(Q(name__contains=query) | Q(description__contains=query) | Q(genre__contains=query))
    else:
        allMovies = Movie.objects.all()

    p = Paginator(allMovies, 6)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    # sending the page object to index.html
    return render(request, 'index.html', context)


def detail(request,id):
    movie = Movie.objects.get(id=id)
    reviews =Review.objects.filter(movie=id).order_by("-comment")
    average = reviews.aggregate(Avg('rating'))['rating__avg']
    if average== None:
        average = 0
    average= round(average,2)
    context ={
        'movie': movie,
        "reviews":reviews,
        "average":average
    }
    return render(request,'details.html', context)


def add_movies(request):
    if request.user.is_authenticated:
        # if request.user.is_superuser:
            if request.method=="POST":
                form=MovieForm(request.POST or None)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.name = request.POST["name"]
                    data.director= request.POST["director"]
                    data.cast= request.POST["cast"]
                    data.description= request.POST["description"]
                    data.release_date= request.POST["release_date"]
                    data.image= request.POST["image"]
                    data.genre = request.POST["genre"]
                    data.user = request.user
                    data.save()
                    return redirect('movieapp:home')
            else:
                form=MovieForm()
            return render(request,'addmovies.html',{"form":form, "controller":"Add Movies"})
        #if they are not admin
        # else:
        #     return redirect("movieapp:home")
    #if they are not logged in
    return redirect("credentials:login")


def edit_movies(request,id):
    if request.user.is_authenticated:
        # if request.user.is_superuser:
            movie=Movie.objects.get(id=id)
            if request.method=="POST":
                form=MovieForm(request.POST or None, instance=movie)
                if form.is_valid():
                    date=form.save(commit=False)
                    date.save()
                    return redirect("movieapp:detail", id)
            else:
                form=MovieForm(instance=movie)
            return render(request,'addmovies.html',{"form":form, "controller":"Edit Movies"})
        # if they are not admin
        # else:
        #     return redirect("movieapp:home")
    # if they are not logged in
    return redirect("credentials:login")


def delete_movies(request,id):
    if request.user.is_authenticated:
        # if request.user.is_superuser:
            movie=Movie.objects.get(id=id)
            movie.delete()
            return redirect("movieapp:home", id)
        #if they are not admin
        # else:
        #     return redirect("movieapp:home")
    #if they are not logged in
    return redirect("credentials:login")


def add_review(request,id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect('movieapp:detail',id)
        else:
            form = ReviewForm()
        return render(request, 'details.html', {"form":form})
    else:
        return redirect("credentials:login")


def edit_review(request,movie_id,review_id):
    if request.user.is_authenticated:
        movie=Movie.objects.get(id=movie_id)
        review = Review.objects.get(movie=movie,id = review_id)

        #checking if review is done by logged user
        if request.user==review.user:
            #grant permission
            if request.method=="POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or ( data.rating <0):
                        error = "Out of range. Please select rating from 0 to 10"
                        return render(request, 'editreview.html', {"error":error, "form":form})
                    else:
                        data.save()
                        return redirect("movieapp:detail", movie_id)
            else:
                form =ReviewForm(instance=review)
            return render(request,'editreview.html', {"form":form})
        else:
            return redirect("movieapp:detail", movie_id)
    else:
        return redirect("credentials:login")


def delete_review(request,movie_id,review_id):
    if request.user.is_authenticated:
        movie=Movie.objects.get(id=movie_id)
        review = Review.objects.get(movie=movie,id = review_id)

        #checking if review is done by logged user
        if request.user==review.user:
            review.delete()
        return redirect("movieapp:detail", movie_id)

    else:
        return redirect("credentials:login")

