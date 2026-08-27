import hashlib
target = '51f8aea8517e3c5b9f5f1c9744f24c3c'
words = ['cssa','CSSA','Cssa','comphrehensive','Comphrehensive','advisor','Advisor','database','Database',
'bushbash','BushBash','bushbash2026','BushBash2026','vals','Vals','VALS','flag','Flag','FLAG','service',
'Service','selection','Selection','comprehensive','Comprehensive','csssa','admin1','Admin123','admin!',
'Password1','root123','toor','changeme123','password123','p@ssw0rd','letmein123','welcome123','ilovebush',
'lostinthebush','findmyway','whereami','whereareyou','iamlost','geolocate','findlocation','vals123','1234567890']
for w in words:
    if hashlib.md5(w.encode()).hexdigest() == target:
        print('FOUND', w)
print('checked', len(words))
