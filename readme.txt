Yazılmış kodun doğru şekilde çalışması için öncelikle proje1.py içerisinde ki

" model_dir = r" "  # Eğitilmiş modelin bulunduğu dizin "

kısıma proje dosyasının içinde bulunan results dosyasını açınız daha sonrasında results dosyasının
içindeki chcekpoint-393 adlı dosyanın yolunu kopyalayarak kod içerisinde model_dir değişkeninin içerisine
tırnaklar arasına yapıştırmanız gerekmektedir.

model_dir = r"C:\\Users\\sedtt\\mulakat_proje\\results\\chcekpoint-393" yazım tarzının bu şekilde olmasına dikkat ediniz.

Eğer Unix terminalde çalıştırırken 

Traceback (most recent call last):
File "C:\Users\ben\Desktop\proje\proje1.py", line 24, in <module>
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
ModuleNotFoundError: No module named 'transformers'

bu şekilde bir hata alırsanız dosyanın olduğu konumda 'pip install  transformers nltk bs4' kodu çalıştırınız, hatayı çözüp tekrar projeyi çalıştırarak projeyi açabilirsiniz.


melike yağcı
0554 593 7238