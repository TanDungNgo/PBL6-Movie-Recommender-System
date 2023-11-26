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
                    request.session['user_id'] = user.id
                    request.session['user_username'] = user.username
                    request.session['user_email'] = user.email
                    request.session['user_firstname'] = user.first_name
                    request.session['user_lastname'] = user.last_name
                    if user.is_superuser:
                        request.session['user_role'] = 'admin'
                    else:
                        request.session['user_role'] = 'user'

                    default_avatar_path = 'https://cdn-icons-png.flaticon.com/512/4998/4998641.png'
                    request.session['user_avatar'] = default_avatar_path
                    
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

@api_view(['GET', 'POST'])
def profile(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            try:
                user_id = request.session['user_id']
                user = User.objects.get(id=user_id)

                first_name = request.POST.get('first_name', user.first_name)
                last_name = request.POST.get('last_name', user.last_name)
                username = request.POST.get('username', user.username)
                email = request.POST.get('email', user.email)

                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                # Check if the username already exists
                if User.objects.exclude(id=user_id).filter(username=username).exists():
                    messages.error(request, 'Username already exists. Please choose a different one.')
                    return redirect('profile')
                
                # Check if the email already exists
                if User.objects.exclude(id=user_id).filter(email=email).exists():
                    messages.error(request, 'Email already exists. Please use a different one.')
                    return redirect('profile')

                # Lấy mật khẩu hiện tại của người dùng từ database
                current_password = User.objects.get(id=user_id).password

                # So sánh mật khẩu cũ
                if not check_password(old_password, current_password):
                    messages.error(request, 'Old password is incorrect.')
                    return redirect('profile')

                # Kiểm tra xác nhận mật khẩu mới
                if new_password != confirm_password:
                    messages.error(request, 'New password and confirm password do not match.')
                    return redirect('profile')

                # Cập nhật mật khẩu mới
                user = User.objects.get(id=user_id)
                user.set_password(new_password)

                # Validate input data here (e.g., email format, phone number format)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                request.session.update({
                    'user_username': username,
                    'user_email': email,
                    'user_first_name': first_name,
                    'user_last_name': last_name,
                })

                user_data = {
                    'username': username,
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }

                # Cập nhật session auth hash để tránh logout người dùng sau khi thay đổi mật khẩu
                update_session_auth_hash(request, user)

                messages.success(request, 'Successfully updated')
                return redirect('profile')

            except User.DoesNotExist:
                messages.error(request, 'User not found')
                return HttpResponse(status=404)
        else:
            messages.error(request, 'Please login')
            return redirect('login')
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

@login_required
def change_password(request):
    if request.method == 'POST':
        user_id = request.user.id  # Lấy id của người dùng từ request
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Lấy mật khẩu hiện tại của người dùng từ database
        current_password = User.objects.get(id=user_id).password

        # So sánh mật khẩu cũ
        if not check_password(old_password, current_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('profile')

        # Kiểm tra xác nhận mật khẩu mới
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('profile')

        # Cập nhật mật khẩu mới
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()

        # Cập nhật session auth hash để tránh logout người dùng sau khi thay đổi mật khẩu
        update_session_auth_hash(request, user)

        messages.success(request, 'Password updated successfully.')
        return redirect('profile')

    return render(request, 'account/profile.html')
