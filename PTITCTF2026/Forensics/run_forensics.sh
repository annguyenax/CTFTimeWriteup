#!/bin/bash
apt-get update && apt-get install -y steghide outguess binwalk libimage-exiftool-perl ruby rubygems curl
gem install zsteg

cat << 'WORDLIST' > words.txt
quantrong
quan_trong
quan trọng
Quan trọng
anhcd05
anhcd
sieungau
sieu_ngau
ủng hộ
ungho
sontungmtp
Sơn Tùng M-TP
haytraochoanh
Hãy Trao Cho Anh
snoopdogg
WORDLIST

echo "--- EXIFTOOL anhcd ---"
exiftool /data/anhcd/solve/anhcd_better.jpg
exiftool /data/anhcd/solve/anhcd.png

echo "--- ZSTEG anhcd.png ---"
zsteg -a /data/anhcd/solve/anhcd.png | grep -i ptitctf

echo "--- STEGHIDE / OUTGUESS anhcd_better.jpg ---"
while read p; do
    steghide extract -sf /data/anhcd/solve/anhcd_better.jpg -p "$p" -f 2>/dev/null && echo "Steghide anhcd found: $p"
    outguess -k "$p" -r /data/anhcd/solve/anhcd_better.jpg out.txt 2>/dev/null && [ -s out.txt ] && echo "Outguess anhcd found: $p" && cat out.txt
done < words.txt

echo "--- STEGHIDE chall.wav ---"
while read p; do
    steghide extract -sf /data/sontung/solve/chall.wav -p "$p" -f 2>/dev/null && echo "Steghide wav found: $p"
done < words.txt

echo "--- BINWALK ---"
binwalk /data/anhcd/solve/anhcd_better.jpg
binwalk /data/sontung/solve/chall.wav
