from re import match
from django.views import View 
from django.http import JsonResponse
from django.shortcuts import render
from .models import Item, User, Movie, Rentals


# Home should have links


# class Home(View):
#   def get(self, request):
#     items = Item.objects.all().values()
#     return render(request,"home.html",{"items":items})
#   def post(self, request):
#     i = Item(name=request.POST["name"],code=request.POST["code"])
#     i.save()
#     items = Item.objects.all().values()
#     return render(request,"home.html",{"items":items})

def home(request):
    return render(request, "home.html")

def account(request):
    return render(request, "creation.html")

def movie(request):
    return render(request, "movies.html")

def rent(request):
    return render(request, "rent.html")

class RentalsHandler(View):
    def get_rentals(self, email):
        rentals = list(Rentals.objects.all().values())  # type: ignore
        if email:
            rentals = list(filter(lambda r: r['user_id'] == email, rentals))
        return rentals

    def get(self, request):
        email = request.GET['email']
        rentals = self.get_rentals(email)
        return JsonResponse({"user": email, "rentals": rentals}, safe=False)

    def post(self, request):
        movie = request.POST.get('movie')
        email = request.POST.get('email')
        action = request.POST.get('action')
        if action == "return":
            rental = Rentals.objects.get(user__email=email, movie__name=movie) # type: ignore
            rental.delete()
            return JsonResponse({"status": 200, "message": "Movie returned!"})
        else:
            # a user cannot rent a movie more than once
            user_rentals = self.get_rentals(email)
            if movie in map(lambda r: r['movie_id'], user_rentals):
                return JsonResponse({"status": "409", "message": "Can only checkout at most one copy of each movie"})
            if len(user_rentals) == 3:
                return JsonResponse({"status": "409", "message": "Can only rent upto 3 movies at a time"})
            user = User.objects.filter(email=email)[0]  # type: ignore
            movie = Movie.objects.filter(name=movie)[0] # type: ignore
            rental = Rentals(user=user, movie=movie)
            rental.save()
            return JsonResponse({"status": 200, "message": "Movie checked!"})

class UserHandler(View):
    def get(self, request):
        email = request.GET['email']
        user = User.objects.filter(email=email)[0]  # type: ignore
        if not user:
            return JsonResponse({"status": 409, "message": "User doesn't exists", "user": {"first_name": "", "last_name": ""}}, safe=False)
        return JsonResponse({"status": 200, "message": "", "user": {"first_name": user.first_name, "last_name": user.last_name}}, safe=False)

    def post(self, request):
        email = request.POST['email']
        if User.objects.filter(email=email).exists():  # type: ignore
            return JsonResponse({"status": 409, "message": "User Already exists"}, safe=True)
        user = User(email=email, first_name=request.POST['first_name'], last_name=request.POST['last_name'])
        user.save()
        return JsonResponse({ "status": 200, "message": "User created!"})

def getChecked(movie):
        rentals = list(Rentals.objects.all().values()) # type: ignore
        checked = list(filter(lambda r: r['movie_id'] == movie['name'], rentals))
        return len(checked)

class MoviesHandler(View):
    def get(self, request):
        movies = list(Movie.objects.all().values())  # type: ignore
        movies = [dict(movie, **{'checked': getChecked(movie)}) for movie in movies]
        return JsonResponse(movies, safe=False)

    def post(self, request):
        action = request.POST['action']
        if action == "new":
            if Movie.objects.filter(name=request.POST['name']).exists():  # type: ignore
                return JsonResponse({"status": 409, "message": "Movie title already exists"})
            movie = Movie(name=request.POST['name'], stock=1)
            movie.save()
            return JsonResponse({'status':200, 'message': "Movie created"})
        else:
            movie = Movie.objects.filter(name=request.POST['movie'])[0] # type: ignore
            movie.stock = movie.stock + (1 if action == "add" else -1)
            movie.save()
            return JsonResponse({'status':200, 'message': "stock updated"})

        return JsonResponse({'status':400, 'message': 'invalid action'})

