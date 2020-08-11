#Kullanacağımız kütüphaneleri projemize dahil ediyoruz.
import cv2
import numpy as np
import pandas as pd
import argparse

# Komut satırından görüntü yolu almak için bağımsız değişken ayrıştırıcısı oluşturma
ap = argparse.ArgumentParser()
#Çalışma şeklini ayarlıyoruz
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#OpenCv ile görüntü okuma işlemi gerçekleşir. Eğer görüntüde sıkıntı çıkarsa boş matris döndürme işlemi yapar
img = cv2.imread(img_path)
#matris için değişkenler
clicked = False
r = g = b = xpos = ypos = 0
#.csv (excel) dosyalarının pandas ile okunmasını sağlamak
#Csv dosyasını pandalarla okuma ve her sütuna ad verme
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#fonksiyon tüm renklerden minimum mesafeyi hesaplamak ve en uygun rengi elde etmek için
def renk(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#Renk adını algılamak ve göstermek için mouse bir görüntünün üzerine geldiğinde bir geri arama etkinliği ayarlayın.

def draw(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
 # Renk adını algılamak ve göstermek için mouse ile bir görüntünün üzerine geldiğinde bir geri arama etkinliği ayarlayın.
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw)
#Pencerede görüntü gösteriliyor ve görüntüye çift tıklatıldığında, görüntü penceresinde renk adı ve RGB değerleri gösterilecek.
while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        # cv2.rectangle (resim, başlangıç ​​noktası, bitiş noktası, renk, kalınlık) -1 tüm dikdörtgeni doldurur
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        # Görüntülenecek metin dizesi oluşturma (Renk adı ve RGB değerleri)
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        # cv2.putText (img, metin, başlangıç, yazı tipi (0-7), fontScale, renk, kalınlık, lineType)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        # Çok açık renkler için metni siyah renkte göstereceğiz
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

        # Kullanıcı 'Q' (ASCİİ değer 81'dir) tuşuna bastığında döngüyü kır
    if cv2.waitKey(20) & 0xFF ==81:
        break
    
cv2.destroyAllWindows()
