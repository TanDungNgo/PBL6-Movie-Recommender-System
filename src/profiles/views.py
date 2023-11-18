from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login

from django.contrib.auth import get_user_model

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

        # Nếu không có lỗi, tạo một đối tượng MyUser và lưu vào cơ sở dữ liệu
        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password)
        user.save()

        # Bạn có thể thêm mã xử lý khác ở đây, chẳng hạn như xử lý avatar và role

        # Chuyển hướng người dùng sau khi đăng ký thành công
        messages.success(request, 'Signup successfully.')
        return redirect('login')  # Thay 'success_page' bằng URL bạn muốn chuyển hướng đến sau khi đăng ký

    return render(request, 'account/signup.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logout successfully.')
    return redirect('signin')

# @api_view(['GET', 'POST'])
# def profile(request):
#     if request.method == 'POST':
#         # Kiểm tra xem người dùng đã đăng nhập chưa
#         if 'user_id' in request.session and 'user_email' in request.session:
#             # Thu thập dữ liệu từ yêu cầu POST
#             user_id = request.session['user_id']
#             user = MyUser.objects.get(id=user_id)

#             # Lấy dữ liệu hiện tại của người dùng
#             current_username = user.username

#             # Lấy giá trị từ yêu cầu POST hoặc sử dụng giá trị hiện tại nếu không có thay đổi
#             firstname = request.POST.get('firstname', user.firstname)
#             lastname = request.POST.get('lastname', user.lastname)
#             phonenumber = request.POST.get('phonenumber', user.phonenumber)
#             country = request.POST.get('country', user.country)
#             new_username = request.POST.get('username', current_username)
#             email = request.POST.get('email', user.email)

#             try:
#                 # Cập nhật thông tin người dùng trong cơ sở dữ liệu
#                 user.firstname = firstname
#                 user.lastname = lastname
#                 user.phonenumber = phonenumber
#                 user.country = country
#                 user.username = new_username
#                 user.email = email

#                 user.save()

#                 # Cập nhật session data
#                 request.session['user_username'] = new_username
#                 request.session['user_email'] = email
#                 request.session['user_firstname'] = firstname
#                 request.session['user_lastname'] = lastname
#                 request.session['user_phonenumber'] = phonenumber
#                 request.session['user_country'] = country

#                 # Trả về dữ liệu đã cập nhật cho phía client
#                 user_data = {
#                     'username': new_username,
#                     'email': email,
#                     'firstname': firstname,
#                     'lastname': lastname,
#                     'phonenumber': phonenumber,
#                     'country': country,
#                 }

#                 return JsonResponse(user_data)
#             except MyUser.DoesNotExist:
#                 return HttpResponse("User not found")
#         else:
#             # Người dùng chưa đăng nhập, xử lý lỗi tại đây
#             messages.error(request, 'Please login')
#             return redirect('signin')
#     else:
#         # Nếu phương thức là GET, thực hiện logic hiển thị thông tin người dùng
#         if 'user_id' in request.session and 'user_email' in request.session:
#             # Fetch user information from the session
#             user_session_data = {
#                 'id': request.session['user_id'],
#                 'role': request.session.get('user_role'),
#                 'email': request.session.get('user_email'),
#                 'firstname': request.session.get('user_firstname'),
#                 'lastname': request.session.get('user_lastname'),
#                 'phonenumber': request.session.get('user_phonenumber'),
#                 'country': request.session.get('user_country'),
#             }

#             return render(request, 'profile.html', user_session_data)
#         else:
#             # Session doesn't exist, redirect to the login page
#             messages.error(request, 'Please login')
#             return redirect('signin')
