from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required



class SignupPageView(View):
    """
        endpoint: /signup
        purpose: "handles signup of an user"
    """
    def get(self, request):
        """

        :param request: None
        :return: render signup form with fields email, first_name, last_name, passowrd
        """
        template_name = 'signup.html'
        context = {"signup_page": "active"}
        return render(request, template_name=template_name, context=context)

    def post(self, request):
        """
        :param request: email and password, confirm_password are mandatory to this api
        :return: sends success message if signup success, else display error messages
        """
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        c_password = request.POST.get('password_confirmation')
        if c_password != password:
            context = {"signup_page": "active", "messages": {"level": "danger", "short": "Error!",
                                                             "msg": "Password doesn't match with confirm password"}}
            return render(request, template_name='signup.html', context=context)

        user = User.objects.filter(username=email)

        if user.exists():
            context = {"signup_page": "active", "messages": {"level": "danger", "short": "Error!",
                                                             "msg": "Email address already exists"}}
            return render(request, template_name='signup.html', context=context)
        elif email and password:
            u = User()
            u.username = email
            u.email = email
            u.first_name = first_name
            u.last_name = last_name
            u.set_password(password)
            u.save()
            context = {"signup_page": "active", "message": {"level": "success", "short": "Success!",
                                                            "msg": "User Created Successfully"}}
            return render(request, template_name='signup.html', context=context)

        return


class LoginPageView(View):
    """
        endpoint: /login
        purpose: to authenticate users
    """

    def get(self, request):
        """
        :param request: None
        :return: render login form with username and password fields
        """
        template_name = 'login.html'
        context = {"login_page": "active"}
        return render(request, template_name=template_name, context=context)

    def post(self, request):
        """
        :param request: email, password are needed to authenticate
        :return: if login success redirect to another page else display error message
        """

        template_name = 'login.html'
        context = {"login_page": "active"}
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user is not None:
            # A backend authenticated the credentials
            user = authenticate(username=username, password=password)
            if user and user.is_authenticated:
                login(request, user)
                context["messages"] = {"msg": "login successful", "level": "success", "short": "Success! "}
                return redirect(self.request.GET.get('next', '/'))

            else:
                context["messages"] = {"msg": "wrong password", "level": "danger", "short": "Error! "}
                return render(request=request, template_name=template_name, context=context)
        else:
            # No backend authenticated the credentials
            context["messages"] = {"msg": "User not found", "level": "danger", "short": "Error! "}
            return render(request=request, template_name=template_name, context=context)


class LogoutView(View):
    """
        endpoint: /logout
        purpose: Handles logout of an user
    """
    def get(self, request):
        """
        :param request: request headers
        :return: renders login page
        """
        logout(request)
        return redirect('/login')


class AboutPageView(View):
    """
        endpoint: /about
        purpose: this handles about page views
    """

    def get(self, request):
        """
        :param request: None
        :return: render about page
        """
        template_name = 'about.html'
        context = {"about_page": "active"}
        return render(request=request, template_name=template_name, context=context)


class HomePageView(View):
    """
        endpoint: /
        purpose: this handles Home page views
    """
    def get(self, request):
        """
        :param request: None
        :return: render home page
        """
        template_name = 'home.html'
        context = {"home_page": "active"}
        return render(request=request, template_name=template_name, context=context)


class Fileupload(View):
    """
            endpoint: /upload
            purpose: this handles file uploads views
        """

    def get(self, request):
        """
        :param request: None
        :return: render upload page
        """
        template_name = 'upload.html'
        context = {"upload_page": "active"}
        return render(request=request, template_name=template_name, context=context)

    def post(self, request):
        """
        :param request: files and return link
        :return: render file  page
        """
        template_name = 'upload.html'

        context = {}
        print(request.FILES)
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location='uploads/')
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            context ={"upload_page": "active", "messages": {"level": "success", "msg": "File Uploaded Successfully",
                                                           "short": "Success! "}}
        else:
            context = {"upload_page": "active", "messages": {"level": "danger", "msg": "No files found",
                                                            "short": "Error! "}}
        return render(request=request, template_name=template_name, context=context)