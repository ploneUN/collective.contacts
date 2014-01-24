"""Definition of the Group content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IGroup
from collective.contacts.config import PROJECTNAME

from collective.contacts.interfaces import IAddressBook
from Acquisition import aq_parent
from Products.CMFCore.interfaces import ISiteRoot


GroupSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ReferenceField(
        name='persons',
        storage = atapi.AnnotationStorage(),
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Persons"),
            description=_(u"The persons that belong to this group"),
            restrict_browsing_to_startup_directory=True,
            startup_directory_method='getAddressBookPath',
        ),
        searchable=1,
        relationship='group_person',
        allowed_types=('Person',),
        multiValued=True,
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

GroupSchema['title'].storage = atapi.AnnotationStorage()
GroupSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(GroupSchema, moveDiscussion=False)

class Group(base.ATCTContent):
    """Let you have several persons together"""
    implements(IGroup)

    portal_type = "Group"
    schema = GroupSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    persons = atapi.ATReferenceFieldProperty('persons')

    def getAddressBook(self):
        parent = aq_parent(self)

        if not parent:
            return None

        while not ISiteRoot.providedBy(parent):
            if IAddressBook.providedBy(parent):
                return parent
            parent = aq_parent(parent)

        return None

    def getAddressBookPath(self):
        parent = self.getAddressBook()
        if parent:
            return '/'.join(parent.getPhysicalPath())
        return ''


atapi.registerType(Group, PROJECTNAME)
