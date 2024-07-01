from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, ClubActivity
from django.contrib.auth.decorators import login_required # login olmadan bu sayfaya giremessin demek.
from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
from . forms import ClubActivityForm 
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import Group # type: ignore

def toggle_activity(request, activity_id):
    activity = get_object_or_404(ClubActivity, id=activity_id)
    activity.activity_is_active = not activity.activity_is_active
    activity.save()
    return JsonResponse({'status': 'success'})



def create_activity(request):
    if request.method == 'POST':
        form = ClubActivityForm(request.POST, request.FILES)
        if form.is_valid():
            # Form verilerini işle
            activity_header = form.cleaned_data['activity_header']
            activity_content = form.cleaned_data['activity_content']
            activity_image = form.cleaned_data['activity_image']
            activity_club = form.cleaned_data['activity_club']
            activity_date = form.cleaned_data['activity_date']
            
            # Bu verilerle yeni bir ClubActivity nesnesi oluştur
            club_activity = ClubActivity.objects.create(
                activity_header=activity_header,
                activity_content=activity_content,
                activity_image=activity_image,
                activity_club=activity_club,
                activity_date=activity_date
            )
            
            # Başka bir işlem yapmak için yönlendirme yapabilirsiniz
    else:
        form = ClubActivityForm()
    return render(request, 'admin/add_activity.html', {'form': form,})

def home(request):
    clubs = Club.objects.all()
    search = request.GET.get('search')
    if search:
        clubs = clubs.filter(Q(club_name__icontains= search),# büyük kücük yazı farketmeksizin.#search burda döngümüz.
                             Q(club_description__icontains = search))
    context = {
       'clubs': clubs,
    }
    return render(request, 'home.html', context)

def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    context = {
        'club': club,
    }
    return render(request, 'detail.html', context)

def club_activity(request, club_id):

    club = get_object_or_404(Club, id=club_id)
    activities_in_club = ClubActivity.objects.filter(activity_club=club)
    context = {
        'club': club,
        'activities_in_club': activities_in_club,
    }
    return render(request, 'activities.html', context)

def haberler(request):
    activities = ClubActivity.objects.all()

    context = {
        'activities':activities,
    }#yukarda activities htmldeki karsılıgıdır oraya istesek herhangi bir baska seyde yazabilirdik.
    return render(request, 'haberler.html', context)

@login_required
def student_home(request):
    return render(request, 'student/student_home.html')


def student_login(request):
    if request.method == 'POST':
        #yukarda / dan sonrakiler gözükmesini istemiyosak post kullanırız gözükmesini istiyosak get kullanırız.
        username = request.POST["username"]#username degiskenine request.POST yaptık icinede htmldeki karsılıgı koyucagımız username ismi verdik.
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        # user diye bir degiskene authenticate(request),yani oturum acma istegi yolladık username=username ve password=passworddir ve
        #bu degiskeni user a esitle.

        if user is not None and user.groups.filter(name='student').exists():
            #eger bir kullanıcım varsa yani none degilse , ve bu kullanıcımın gurubu student isimli guruba dahilse.
            login(request, user)
            #user degiskenini login et. ve home sayfasına gönder.
            return redirect("home")# redirect kullanımda urls.pydeki name isimli degiskeni buraya yazarız.
        else:
            return render(request, 'student/student_login.html', {
                "error": "Kullanıcı adı veya parola yanlış."
            })
    return render(request, 'student/student_login.html')

def student_logout(request):
    logout(request)
    return redirect('home')

@login_required
def admin_home(request):
    return render(request, 'admin/admin_home.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name='club manager').exists():
            login(request, user)
            return redirect("admin-home")
        else:
            return render(request, 'admin/admin_login.html', {
                "error": "Kullanıcı adı veya parola yanlış."
            })
    return render(request, 'admin/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin-login')

@login_required#bu dekoratörü kullanarak, bu görünüm fonksiyonunun yalnızca giriş yapmış kullanıcılar tarafından erişilebilir olduğunu belirtir
def sks_home(request):
    activities = ClubActivity.objects.all()
    activity_formset = [ClubActivityForm(prefix=str(activity.id)) for activity in activities]

    if request.method == 'POST':
        for form in activity_formset:
            if form.is_valid(): # eger böyle bi form gecerliyse 
                form.save() # formu kaydet
        return redirect('sks-home')
    return render(request, 'sks/skss_home.html', {'activities': activities, 'activity_formset': activity_formset})
#bunlarıda sks/skss_home.html de kullanıyoruz.


def sks_login(request):
    if request.method == 'POST':#gelen istegin post yöntemiylemi yoksa get yöntemiylemi gelecegini söylüyor ...
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)#Bu fonksiyon, verilen kullanıcı adı ve şifreyle eşleşen bir kullanıcı varsa, bu kullanıcı nesnesini döndürür.
        #Aksi halde None değeri döner.
        if user is not None and user.groups.filter(name='sks admin').exists():# burdada üsteki user eslemesi yapıldıktan sonra user eslesmesi dogruysa bu if bloguna giricek.
            login(request, user)
            return redirect('sks-home')#Kullanıcı başarılı bir şekilde giriş yaptığında, sks-home adlı URL'ye yönlendirilir.
        else:
            return render(request, 'sks/sks_login.html', {
                "error": "Kullanıcı adı veya parola yanlış."
            })
    return render(request, 'sks/sks_login.html')
    #Eğer HTTP isteği POST yöntemiyle gelmemişse, yani kullanıcı henüz bir form göndermemişse veya formda hata varsa, bu durumda giriş sayfasını kullanıcıya gösterir.


def sks_logout(request):
    logout(request)
    return redirect('sks-login')




