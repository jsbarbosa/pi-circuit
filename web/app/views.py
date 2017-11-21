from django.shortcuts import render
from app.forms import NewUserForm

# Create your views here.
def index(request):
    # my_dict = {'insert_me':"Now I am coming from first_app/index.html!"}
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # first_name = 
            # last_name = models.CharField(max_length=128)
            # email = models.EmailField(max_length=254,unique=True)
            return render(request, 'app/index.html')
        else:
            print("FALSE")
    return render(request, 'app/index.html', context={'form':form})
