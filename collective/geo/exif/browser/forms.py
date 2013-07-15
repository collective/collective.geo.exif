import logging
logger = logging.getLogger('collective.geo.exif')
from PIL import Image

from five.formlib import formbase

from zope import interface, schema
from zope.formlib import form

from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
from collective.geo.exif.readexif import get_exif_data, get_lat_lon


class IExifSchema(interface.Interface):
    custom_icon = schema.TextLine(
        title=u'Custom Icon',
        description=u'Expression to display the placemark on the map',
        required=False,
        readonly=False,
        default=u'image_thumb',
        missing_value=u'image_thumb',
        )

class ExtractExifForm(formbase.PageForm):
    form_fields = form.FormFields(IExifSchema)
    # Put here the label to be displayed as form title
    label = u'Extract Exif Data'
    # Put here the form description to be displayed under the form title
    description = u'Geoannotate Image with EXIF information'

    # Instead of 'Submit button' put here the label of the form submit button
    @form.action('Submit', failure='handle_failure')
    def handle_success(self, action, data):
        """
        Called when the action was submitted and there are NO validation
        errors.

        This form is generated with ZopeSkel. Please make sure you fill in
        the implementation of the form processing.

        """
        # Put here the feedback to show in case the form submission succeeded
        geo = IGeoManager(self.context)
        style = IGeoCustomFeatureStyle(self.context)
        image = Image.open(self.context.getFile().getIterator())
        exif_data = get_exif_data(image)
        lat, lon = get_lat_lon(exif_data)
        if lat and lon and geo.isGeoreferenceable():
            geo.setCoordinates('Point', (lon, lat))
            style.geostyles.data['use_custom_styles']=True
            import ipdb; ipdb.set_trace()
            if data.get('custom_icon'):
                url = 'string:' + self.context.absolute_url() + '/'
                style.geostyles.data['marker_image'] = url + data['custom_icon']
                style.geostyles.data['marker_image_size'] = 1.0
            style.geostyles.update(style.geostyles)
            self.status = 'Coordinates set'
        else:
            self.status = 'Image has no EXIF GPS information'
        url = self.context.absolute_url()
        url += '/view'
        self.request.response.redirect(url)

    def handle_failure(self, action, data, errors):
        """
        Called when the action was submitted and there are validation errors.

        """
        # Put here the feedback message to show in case the validation failed
        self.status = 'Errors occured while submitting the form'


    @form.action('Cancel')
    def actionCancel(self, action, data):
        url = self.context.absolute_url()
        url += '/view'
        self.request.response.redirect(url)
