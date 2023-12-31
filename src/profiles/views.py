from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser

User = get_user_model()

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    user = CustomUser.objects.get(email=email)
                    request.session['user_id'] = user.id
                    request.session['user_username'] = user.username
                    request.session['user_email'] = user.email
                    request.session['user_firstname'] = user.first_name
                    request.session['user_lastname'] = user.last_name
                    if user.is_superuser:
                        request.session['user_role'] = 'admin'
                    else:
                        request.session['user_role'] = 'user'
                    if user.avatar:
                        request.session['user_avatar'] = user.avatar
                    else:
                        request.session['user_avatar'] = 'https://cdn-icons-png.flaticon.com/512/4998/4998641.png'
                    
                    messages.success(request, 'Login successfully.')
                    if user.is_superuser:
                       return redirect('dashboard')
                    
                    return redirect('home')
                else:
                    messages.error(request, 'Email or password is incorrect.')
            except User.DoesNotExist:
                messages.error(request, 'Email or password is incorrect.')
        else:
            messages.error(request, 'Please enter both email and password.')

    return render(request, 'account/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Kiểm tra xem các trường đã điền đầy đủ hay chưa và hiển thị thông báo lỗi nếu cần
        if not username:
            messages.error(request, 'Username is required.')
        if not email:
            messages.error(request, 'Email is required.')
        if not password:
            messages.error(request, 'Password is required.')

        # Kiểm tra xem có thông báo lỗi hay không
        if messages.get_messages(request):
            return render(request, 'account/signup.html')

        # Kiểm tra xem username hoặc email đã tồn tại trong cơ sở dữ liệu chưa
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'account/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'account/signup.html')

        # Nếu không có lỗi và username, email đều chưa tồn tại, tiến hành tạo người dùng mới
        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password)
        CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Bạn có thể thêm mã xử lý khác ở đây, chẳng hạn như xử lý avatar và role

        # Chuyển hướng người dùng sau khi đăng ký thành công
        messages.success(request, 'Signup successfully.')
        return redirect('signin')  # Thay 'signin' bằng URL bạn muốn chuyển hướng đến sau khi đăng ký

    return render(request, 'account/signup.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logout successfully.')
    return redirect('signin')

@api_view(['GET'])
def profile(request):
        if 'user_id' in request.session:
            user_session_data = {
                'id': request.session['user_id'],
                'email': request.session.get('user_email'),
                'first_name': request.session.get('user_firstname'),
                'last_name': request.session.get('user_lastname'),
            }
            return render(request, 'account/profile.html', user_session_data)
        else:
            messages.error(request, 'Please login')
            return redirect('signin')

@api_view(['POST'])   
def update_profile(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            try:
                user_id = request.session['user_id']
                user = User.objects.get(id=user_id)
                customuser = CustomUser.objects.get(id=user_id)

                username = request.POST.get('username')
                email = request.POST.get('email')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                
                # Check if the username already exists
                if User.objects.exclude(id=user_id).filter(username=username).exists():
                    messages.error(request, 'Username already exists. Please choose a different one.')
                    return redirect('profile')
                
                # Check if the email already exists
                if User.objects.exclude(id=user_id).filter(email=email).exists():
                    messages.error(request, 'Email already exists. Please use a different one.')
                    return redirect('profile')
                
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email

                user.save()

                customuser.username = username
                customuser.first_name = first_name
                customuser.last_name = last_name
                customuser.email = email

                customuser.save()

                request.session.update({
                    'user_name': username,
                    'user_email': email,
                    'user_firstname': first_name,
                    'user_lastname': last_name,
                })

                messages.success(request, 'Successfully updated.')
                return redirect('profile')

            except User.DoesNotExist:
                messages.error(request, 'User not found')
                return HttpResponse(status=404)
        else:
            messages.error(request, 'Please login')
            return redirect('signin')
    else:
        if 'user_id' in request.session:
            user_session_data = {
                'id': request.session['user_id'],
                'email': request.session.get('user_email'),
                'first_name': request.session.get('user_first_name'),
                'last_name': request.session.get('user_last_name'),
            }

            return render(request, 'account/profile.html', user_session_data)
        else:
            messages.error(request, 'Please login')
            return redirect('signin')
        
@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            try:
                user_id = request.session['user_id']
                user = User.objects.get(id=user_id)
                customuser = CustomUser.objects.get(id=user_id)

                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                current_password = User.objects.get(id=user_id).password

                if not old_password:
                    messages.error(request, 'Please fill in all information.')
                    return redirect('profile')

                if not new_password:
                    messages.error(request, 'Please fill in all information.')
                    return redirect('profile')
                
                if not confirm_password:
                    messages.error(request, 'Please fill in all information.')
                    return redirect('profile')

                if not check_password(old_password, current_password):
                    messages.error(request, 'Old password is incorrect.')
                    return redirect('profile')

                if new_password != confirm_password:
                    messages.error(request, 'New password and confirm password do not match.')
                    return redirect('profile')
                else:
                    user.set_password(new_password)
                    user.save()

                    customuser.set_password(new_password)
                    customuser.save()

                    update_session_auth_hash(request, user)

                    messages.success(request, 'Successfully changed.')
                    return redirect('profile')

            except User.DoesNotExist:
                messages.error(request, 'User not found')
                return HttpResponse(status=404)
        else:
            messages.error(request, 'Please login')
            return redirect('login')