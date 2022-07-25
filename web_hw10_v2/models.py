from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField


class Record(Document):
    name = StringField()
    description = StringField()
    email = StringField()
    phone = StringField()
    address = StringField()
    birthday = StringField()
    created = StringField()
    done = BooleanField(default=True)


class Note(Document):
    body = StringField()
    created = DateTimeField(default=datetime.now())
