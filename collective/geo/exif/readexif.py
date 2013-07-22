# https://gist.github.com/moshekaplan/5330395
import sys
import pytz, datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                print value
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data

def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    deg_num, deg_denom = value[0]
    d = float(deg_num) / float(deg_denom)

    min_num, min_denom = value[1]
    m = float(min_num) / float(min_denom)

    sec_num, sec_denom = value[2]
    s = float(sec_num) / float(sec_denom)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the
    provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None
    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]
        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get('GPSLatitudeRef')
        gps_longitude = gps_info.get('GPSLongitude')
        gps_longitude_ref = gps_info.get('GPSLongitudeRef')
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat *= -1
            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon *= -1
    return lat, lon


def get_altitude(exif_data):
    """ extract altitude if avalaible from the
    provided exif_data (obtained through get_exif_data above)"""
    alt = None
    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]
        gps_altitude = gps_info.get('GPSAltitude')
        gps_altitude_ref = gps_info.get('GPSAltitudeRef')
        if gps_altitude:
            alt = float(gps_altitude[0]) / float(gps_altitude[1])
            if gps_altitude_ref == 1:
                alt *=-1
    return alt

def get_timestamp(exif_data):
    """ extract the timestamp if avalaible as datetime  from the
    provided exif_data (obtained through get_exif_data above)"""
    dt = None
    utc = pytz.utc
    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]
        gps_time_stamp = gps_info.get('GPSTimeStamp')
        if 'GPSDateStamp' in gps_info:
            gps_date = [int(i) for i in gps_info['GPSDateStamp'].split(':')]
        elif 29 in gps_info:
            gps_date = [int(i) for i in gps_info[29].split(':')]
        else:
            gps_date = None
        if gps_time_stamp and gps_date:
            yy = gps_date[0]
            mm = gps_date[1]
            dd = gps_date[2]
            h = int(float(gps_time_stamp[0][0]) / float(gps_time_stamp[0][1]))
            m = int(float(gps_time_stamp[1][0]) / float(gps_time_stamp[1][1]))
            s = int(float(gps_time_stamp[2][0]) / float(gps_time_stamp[2][1]))
            dt = utc.localize(datetime.datetime(yy,mm,dd,h,m,s))
    return dt



################
# Example ######
################
if __name__ == "__main__":
    # load an image through PIL's Image object
    if len(sys.argv) < 2:
        print "Error! No image file specified!"
        print "Usage: %s <filename>" % sys.argv[0]
        sys.exit(1)

    image = Image.open(sys.argv[1])
    exif_data = get_exif_data(image)
    print get_lat_lon(exif_data)
