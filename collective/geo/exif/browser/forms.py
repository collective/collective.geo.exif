import logging
logger = logging.getLogger('collective.geo.exif')

from five.formlib import formbase

from zope import interface, schema
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.geo.exif.utils import set_geoannotation


class IExifSchema(interface.Interface):


    only_images_without_geom = schema.Bool(
        title=u'Only Images without Geometry',
        description=u'Do not overwrite coordinates of images that have geometries',
        required=False,
        readonly=False,
        default=True,
        )

    use_image_as_marker = schema.Bool(
        title=u'Use Image as marker',
        description=u'If checked the image will be set as the marker',
        required=False,
        readonly=False,
        default=True,
        )

    image_size = schema.TextLine(
        title=u'Marker Image Size',
        description=u'Size of the Marker Image (image_thumb 128px, image_tile 64px, image_icon 32px, image_listing 16px)',
        required=False,
        readonly=False,
        default=u'image_icon',
        )

class ExtractExifForm(formbase.PageForm):
    form_fields = form.FormFields(IExifSchema)
    # Put here the label to be displayed as form title
    label = u'Extract Exif Data'
    # Put here the form description to be displayed under the form title
    description = u'Geoannotate Image with EXIF information'

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    def set_exif_as_geoannotation(self, context, use_image_as_marker, image_size):
        if use_image_as_marker and image_size:
            icon_url = 'string:' + context.absolute_url() + '/' + image_size
        else:
            icon_url = None
        success = set_geoannotation(context, icon_url)
        return success

    @form.action('Submit', failure='handle_failure')
    def handle_success(self, action, data):
        """
        Called when the action was submitted and there are NO validation
        errors.

        This form is generated with ZopeSkel. Please make sure you fill in
        the implementation of the form processing.

        """
        # Put here the feedback to show in case the form submission succeeded
        if self.context.portal_type == 'Image':
            success = self.set_exif_as_geoannotation(self.context,
                data.get('use_image_as_marker'), data.get('image_size'))
            if success:
                msg = 'Coordinates set'
            else:
                msg = 'Image has no EXIF GPS information'
        else:
            path = '/'.join(self.context.getPhysicalPath())
            brains = self.portal_catalog(portal_type='Image', path=path)
            i=0
            j=0
            for brain in brains:
                j+=1
                if data.get('only_images_without_geom'):
                    try:
                        if brain.zgeo_geometry['coordinates']:
                            continue
                    except:
                        pass
                obj = brain.getObject()
                success = self.set_exif_as_geoannotation(obj,
                    data.get('use_image_as_marker'), data.get('image_size'))
                if success:
                    i+=1
            msg = 'annotated %i of %i Images' %(i, j)
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
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
