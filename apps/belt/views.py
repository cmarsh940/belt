from django.shortcuts import render, redirect, reverse
from ..login_register.models import User
from django.db.models import Count

# Create your views here.
def index(request):
	if 'user_id' in request.session:
		user = User.objects.get(id=request.session['user_id'])
		# users = User.cu
		# context = {
		# 	'user': user,
		# }

		current_user = User.objects.currentUser(request)
		#finds all of users current friends
		friends = current_user.friends.all()

		# "SELECT * FROM users where id not in (1, 2, 3)"

		users = User.objects.exclude(id__in=friends).exclude(id=current_user.id)

		context = {
			'user': user,
			'users': users,
			'friends': friends,
		}
		return render(request, 'belt/index.html', context)
	return redirect(reverse('landing'))

def user(request, id):
	if 'user_id' in request.session:
		user = User.objects.get(id=id)
		context = {
			'user': user
		}
		
		return render(request, 'belt/show.html', context)
	return redirect(reverse('belt'))

def addFriend(request, id):
    if request.method == "POST":
        if 'user_id' in request.session:
            current_user = User.objects.currentUser(request)
            friend = User.objects.get(id=id)

            current_user.friends.add(friend)

            return redirect(reverse('belt'))

    return redirect(reverse('landing'))



def removeFriend(request, id):
    if request.method == "POST":
        if 'user_id' in request.session:
            current_user = User.objects.currentUser(request)
            friend = User.objects.get(id=id)

            current_user.friends.remove(friend)

            return redirect(reverse('belt'))

    return redirect(reverse('landing'))