from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import bcrypt
from .models import User


# Error handler

def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

# Pages that will be RENDERED

def index(request):

    return render(request, 'login_register/index.html')

#success page that checks if the user id is in sessions befor it allows them to go to page
# if it does not have the id, it will redirect them back home
def success(request):
    if 'user_id' in request.session:
        current_user = User.objects.currentUser(request)
#finds all of users current friends
        friends = current_user.friends.all()

        # "SELECT * FROM users where id not in (1, 2, 3)"

        users = User.objects.exclude(id__in=friends).exclude(id=current_user.id)

        context = {
            'users': users,
            'friends': friends,
        }

        return render(request, 'success', context)

    return redirect(reverse('landing'))

#  Register Handler with requirments Must be a POST method and make sure to check the request

def register(request):
    if request.method == "POST":
        errors = User.objects.validateRegistration(request.POST)

        if not errors:
            user = User.objects.createUser(request.POST)

            request.session['user_id'] = user.id

            return redirect(reverse('belt'))

        flashErrors(request, errors)

    return redirect(reverse('landing'))



#  Login Handler with requirments/ Must be a POST method and make sure to check the request
def login(request):
    if request.method == "POST":
        errors = User.objects.validateLogin(request.POST)

        if not errors:
            user = User.objects.filter(email = request.POST['email']).first()

            if user:
                password = str(request.POST['password'])
                user_password = str(user.password)

                hashed_pw = bcrypt.hashpw(password, user_password)

                if hashed_pw == user.password:
                    request.session['user_id'] = user.id

                    return redirect(reverse('belt'))

            errors.append("Invalid account information.")

        flashErrors(request, errors)

        return redirect(reverse('landing'))


# Logout Handler / check ID through sessions

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')

    return redirect(reverse('landing'))






# Add friend Handler

# def addFriend(request, id):
#     if request.method == "POST":
#         if 'user_id' in request.session:
#             current_user = User.objects.currentUser(request)
#             friend = User.objects.get(id=id)

#             current_user.friends.add(friend)

#             return redirect(reverse('books'))

#     return redirect(reverse('landing'))






# # Remove friend Handler

# def removeFriend(request, id):
#     if request.method == "POST":
#         if 'user_id' in request.session:
#             current_user = User.objects.currentUser(request)
#             friend = User.objects.get(id=id)

#             current_user.friends.remove(friend)

#             return redirect(reverse('success'))

#     return redirect(reverse('landing'))