from django.shortcuts import render
from .forms import ImageUploadForm
import random

def predict(request):
    if request.method == 'GET':
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            #4章で、画像ファイル(img_file)の前処理を追加
            #４章で判定結果のロジックを追加
            #暫定で、ダミーの判定結果としてpredictionにランダムで「猫」か「犬」を格納
            prediction = random.choice(["猫", "犬"])
            return render(request, 'home.html', {'form': form, 'prediction':prediction})
        else:
            orm = ImageUploadForm()
            return render(request, 'home.html', {'form': form})
        