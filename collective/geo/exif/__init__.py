from zope.i18nmessageid import MessageFactory

exifMessageFactory = MessageFactory('collective.geo.exif')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
