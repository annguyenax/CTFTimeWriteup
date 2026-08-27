import base64
s = "eyJzdWIiOjEsInJvbGUiOiJ1c2VyIiwiY2xpZW50Ijoid2ViIn0"
print(base64.urlsafe_b64decode(s + "===").decode('utf-8'))
