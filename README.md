📄 Akıllı Hukuk & Doküman Yönetim Asistanı
Bu proje,LangGraph ve Langchain kullanılarak yapılmıştır 

🚀 Öne Çıkan Özellikler
* 41 milyar aktif parametreye ve toplam 675 milyar parametreye sahip olan Mistral AI modeli ile (mistral-large-latest) yüksek doğrulukta işlem yapabilmektedir
* Streamlit ile geliştirilmiş, kullanıcı dostu chat arayüzü.


🛠️ Kullanılan Teknolojiler

  * Dil Modeli: Mistral AI (Large)

  * Frameworks: LangChain,Langgraph

  * Arayüz: Streamlit

  * Veri Doğrulama: Pydantic (Structured Output)
  
🔧Bu Uygulama Nasıl Çalışıyor?
* Kullanıcı ilk önce bir soru sorar ve LLM soruyu analiz eder ve kullanıcının niyetini anlar ve kullanıcının niyetine göre de (ekleme - silme - sorma - listeleme) yapar

Ekleme Nasıl Yapılıyor?
* Kullanıcı bir sorgu gönderir örneğin (Not al : Bu günlerde Kış geçen yıllara kıyasla daha soğuk olacak)
* Eğer Kullanıcı bir başlık belirtmezse llm tarih atar belirtirse notun başlığı olarak kaydeder ve sözlüğe atar

Silme Nasıl Yapılıyor?
* Kullanıcı silmek istediği dosyanın ismini silmek istiyorum diye yazar örneğin (Judo.txt dosyasını silmek istiyorum)
* LLM, bu dosya ismini çıkarır ve bu dosya ismi eğer sözlükte key olarak varsa siler yoksa silmez

Sorma Nasıl Yapılıyor?
* Kullanıcı belirli bir soru sorar ve LLM bu soruya ilişkin bir bilgi var mi yok mu diye sözlüğe bakar
* Örneğin (Mavi Kediyi kim gördü? Eğer cevap sözlükte var ise ona göre cevap verir, Eğer cevap sözlükte yok ise de cevap bulamadım der

Listeleme Nasıl Yapılıyor?
* Kullanıcı, Tüm notlarımı görmek istiyorum derse ya da bana liste olarak getir derse, Sözlükte bulunan Not Başlıkları ve İçerikleri bir liste olarak karşısına sunulur

⚠️ UYARI
* Bu projede eklenen notlar kesinlikle ve kesinlikle geçicidir ve Program kapatıldığında hepsi ortadan kalkar 
