from .models import Notification, CustomUser
from django.views.decorators.http import require_POST
from .forms import RegisterForm, CustomLoginForm, EmailResetRequestForm, EmailCodeResetForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CarForm
from .models import Car
import random
from django.shortcuts import get_object_or_404
from .models import Car, Rent
from .forms import RentForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from random import randint
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Car




def home(request):
    all_cars = list(Car.objects.all())
    featured_cars = all_cars[:4]  # რჩეულები
    random_cars = random.sample(all_cars, min(4, len(all_cars)))  # შემთხვევითები

    return render(request, 'home.html', {
        'featured_cars': featured_cars,
        'random_cars': random_cars,
    })
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # ვაყენებთ False სანამ არ დაადასტურებს
            user.verification_code = str(randint(100000, 999999))
            user.save()

            # Email გაგზავნა
            send_mail(
                subject='ავტორიზაციის კოდი',
                message=f"თქვენი ავტორიზაციის კოდია: {user.verification_code}",
                from_email='autorent@example.com',
                recipient_list=[user.email],
                fail_silently=False,
            )

            return redirect('verify_email', user_id=user.id)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)  # <-- აქ
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'მომხმარებლის მონაცემები არასწორია')
    else:
        form = CustomLoginForm()  # <-- და აქ
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    initials = f"{user.first_name[0]}{user.last_name[0]}" if user.first_name and user.last_name else "U"

    rented_cars = Rent.objects.filter(user=user)
    added_cars = Car.objects.filter(added_by=user)
    favorite_cars = user.favorite_cars.all()

    return render(request, 'profile.html', {
        'user': user,
        'initials': initials,
        'rented_cars': rented_cars,
        'added_cars': added_cars,
        'favorite_cars': favorite_cars
    })

@login_required
def add_car_view(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.added_by = request.user
            car.save()
            return redirect('home')  # ან car detail page
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


# views.py

def car_filter_view(request):
    cars = Car.objects.all()

    city = request.GET.get('city')
    brand = request.GET.get('brand')
    transmission = request.GET.get('transmission')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if city:
        cars = cars.filter(city__icontains=city)
    if brand:
        cars = cars.filter(brand__icontains=brand)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    if phone_number := request.GET.get('phone_number'):
        cars = cars.filter(added_by__phone_number__icontains=phone_number)

    search_query = request.GET.get('q')
    if search_query:
        cars = cars.filter(brand__icontains=search_query) | cars.filter(model__icontains=search_query) | cars.filter(
            added_by__phone_number__icontains=search_query)

    return render(request, 'filter.html', {'cars': cars})


def car_detail_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})





@login_required
def rent_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            rent = form.save(commit=False)
            rent.user = request.user
            rent.car = car

            start_date = rent.rent_start_date
            end_date = rent.rent_end_date
            num_days = (end_date - start_date).days + 1
            rent.total_price = car.price_per_day * num_days
            rent.save()

            if car.added_by != request.user:
                Notification.objects.create(
                    user=car.added_by,
                    message=f"{request.user.first_name} {request.user.last_name} იქირავა თქვენი მანქანა: {car.brand} {car.model}",
                    link=f"/car/{car.id}/"
                )

            return redirect('rent_success')
    else:
        form = RentForm()

    return render(request, 'rent_car.html', {'form': form, 'car': car})


def rent_success_view(request):
    return render(request, 'rent_success.html')

@require_POST
@login_required
def cancel_rent_view(request, rent_id):
    rent = get_object_or_404(Rent, id=rent_id, user=request.user)
    rent.delete()
    messages.success(request, "დაქირავებული მანქანა გაუქმდა.")
    return redirect('profile')



@login_required
def toggle_favorite_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car in request.user.favorite_cars.all():
        request.user.favorite_cars.remove(car)
    else:
        request.user.favorite_cars.add(car)
    return redirect('car_detail', car_id=car.id)


def user_profile_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_profile.html', {'user': user})


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # ყველა წაკითხულად მონიშნვა
    notifications.update(is_read=True)

    return render(request, 'notifications.html', {'notifications': notifications})


# views.py

def verify_email_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.verification_code:
            user.is_verified = True
            user.is_active = True
            user.verification_code = ''
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "კოდი არასწორია")

    return render(request, 'verify_email.html', {'user': user})



def password_reset_request_view(request):
    if request.method == 'POST':
        form = EmailResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                code = str(random.randint(100000, 999999))
                user.verification_code = code
                user.save()

                send_mail(
                    subject='პაროლის აღდგენის კოდი',
                    message=f'თქვენი პაროლის აღდგენის კოდია: {code}',
                    from_email=None,
                    recipient_list=[email],
                )
                return redirect('reset_password', user_id=user.id)
            except CustomUser.DoesNotExist:
                form.add_error('email', 'მომხმარებელი ამ იმეილით არ არსებობს')
    else:
        form = EmailResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})


def password_reset_verify_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = EmailCodeResetForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == user.verification_code:
                user.set_password(form.cleaned_data['new_password'])
                user.verification_code = ''
                user.save()
                messages.success(request, "პაროლი წარმატებით განახლდა")
                return redirect('login')
            else:
                form.add_error('code', 'კოდი არასწორია')
    else:
        form = EmailCodeResetForm()
    return render(request, 'password_reset_verify.html', {'form': form})

# --- მანქანის წაშლის ფუნქციონალი მხოლოდ ავტორისთვის ---
# core/views.py

@login_required
def delete_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id, added_by=request.user)
    car.delete()
    messages.success(request, "მანქანა წარმატებით წაიშალა")
    return redirect('profile')


from django.shortcuts import render

def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_403_view(request, exception):
    return render(request, 'errors/403.html', status=403)

def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)