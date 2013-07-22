import logging
logger = logging.getLogger('collective.geo.exif')
from PIL import Image

from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
from collective.geo.exif.readexif import get_exif_data, get_lat_lon, get_timestamp


def set_geoannotation(context, icon):
        try:
            geo = IGeoManager(context)
            style = IGeoCustomFeatureStyle(context)
            image = Image.open(context.getFile().getIterator())
            exif_data = get_exif_data(image)
            lat, lon = get_lat_lon(exif_data)
            timestamp = get_timestamp(exif_data)
        except:
            return None
        if lat and lon and geo.isGeoreferenceable():
            geo.setCoordinates('Point', (lon, lat))
            if icon:
                style.geostyles.data['use_custom_styles']=True
                style.geostyles.data['marker_image'] = icon
                style.geostyles.data['marker_image_size'] = 1.0
                style.geostyles.update(style.geostyles)
            logger.info('annotated %s with lat %f, lon %f' % (context.getId(), lat, lon))
            success = True
        else:
            success = False
            logger.info('Image has no EXIF GPS information')
            timestamp = exif_data.get('DateTimeOriginal')
        if timestamp:
            context.setCreationDate(timestamp)
        return success

def handle_add_image(context, event):
    icon_url = 'string:' + context.absolute_url() + '/image_icon'
    set_geoannotation(context, icon_url)
