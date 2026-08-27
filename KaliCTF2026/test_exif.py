from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = {}
        info = image.getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]
                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        return exif_data
    except Exception as e:
        return str(e)

print(get_exif_data(r'D:\download\CTFTimeWriteup\KaliCTF2026\osint\The Last Shift\files\evidence.png'))
