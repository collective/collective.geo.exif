import logging
logger = logging.getLogger('collective.geo.exif')


from five.formlib import formbase

from zope import interface, schema
from zope.formlib import form

from collective.geo.exif.utils import set_geoannotation


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
        icon_url = 'string:' + self.context.absolute_url() + '/' + data.get('custom_icon')
        msg = set_geoannotation(self.context, icon_url)
        self.status = msg
        url = self.context.absolute_url() + '/view'
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
