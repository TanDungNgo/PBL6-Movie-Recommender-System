from django.shortcuts import render, redirect
from .models import MyUser
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Kiểm tra xem email và password đã được nhập
        if email and password:
            try:
                user = MyUser.objects.get(email=email)
                if check_password(password, user.password):
                    # Tạo một phiên làm việc tùy chỉnh
                    request.session['user_id'] = user.id
                    request.session['user_username'] = user.username
                    request.session['user_role'] = user.role
                    request.session['user_email'] = user.email
                    request.session['user_firstname'] = user.firstname
                    request.session['user_lastname'] = user.lastname
                    request.session['user_phonenumber'] = user.phonenumber
                    request.session['user_country'] = user.country

                    
                    # Kiểm tra xem user có avatar không
                    if user.avatar:
                        request.session['user_avatar'] = user.avatar
                    else:
                        # Đặt URL của ảnh mặc định nếu không có avatar
                       default_avatar_path = '/img/avatar.jpg'
                       request.session['user_avatar'] = default_avatar_path  # Thay đổi đường dẫn thành ảnh mặc định của bạn
                    # Điều hướng tới trang tương ứng
                    messages.success(request, 'Login successfully.')
                    if user.role == 'user':
                        # Điều hướng sang trang user
                        return redirect('index')
                    if user.role == 'admin':
                        # Điều hướng sang trang admin
                       return redirect('general')
                    
                else:
                    # Đăng nhập thất bại, hiển thị thông báo lỗi
                    messages.error(request, 'Email or password is incorrect.')
            except MyUser.DoesNotExist:
                # Đăng nhập thất bại, hiển thị thông báo lỗi
                messages.error(request, 'Email or password is incorrect.')
        else:
            # Người dùng chưa nhập thông tin, hiển thị thông báo lỗi
            messages.error(request, 'Please enter both email and password.')

    return render(request, 'profiles/signin.html')

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
            return render(request, 'profiles/signup.html')

        # Nếu không có lỗi, tạo một đối tượng MyUser và lưu vào cơ sở dữ liệu
        hashed_password = make_password(password)
        user = MyUser(username=username, email=email, password=hashed_password)
        user.save()

        # Bạn có thể thêm mã xử lý khác ở đây, chẳng hạn như xử lý avatar và role

        # Chuyển hướng người dùng sau khi đăng ký thành công
        messages.success(request, 'Signup successfully.')
        return redirect('signin')  # Thay 'success_page' bằng URL bạn muốn chuyển hướng đến sau khi đăng ký

    return render(request, 'profiles/signup.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logout successfully.')
    return redirect('signin')  # Điều hướng sau khi đăng xuất (thay 'login' bằng URL của trang đăng nhập của bạn)



