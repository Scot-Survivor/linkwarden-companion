import pydantic
import datetime

from pydantic import root_validator, Field, model_validator
from typing import List, ClassVar, Literal, get_args
from linkwarden_companion.utils import get_all_subclasses

LinkType = Literal["pdf", "image", "url"]
valid_link_types = get_args(LinkType)


class BaseModel(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class Tag(BaseModel):
    id: int
    name: str
    ownerId: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime


class Collection(BaseModel):
    id: int
    name: str
    description: str
    icon: str | None
    iconWeight: str | None
    color: str | None
    parentId: int | None
    isPublic: bool
    ownerId: int
    createdById: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime


class Link(BaseModel):
    verbose_level: ClassVar = {
        0: "\tID: {id} | Name: {name} | URL: {url} | Collection: {collectionId} | Created By: {createdById}",
        1: "\tID: {id} | Name: {name} | URL: {url} | Collection: {collectionId}"
           " | Created By: {createdById} | Description: {description}",
    }

    id: int
    name: str
    type: LinkType
    description: str
    createdById: int
    collectionId: int
    icon: str | None
    iconWeight: str | None
    color: str | None
    url: str
    textContent: str | None
    preview: str | None
    image: str | None
    pdf: str | None
    readable: str | None
    monolith: str | None
    lastPreserved: datetime.datetime | None
    importDate: datetime.datetime | None
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    tags: List[Tag]
    collection: Collection
    pinnedBy: List[int] | None
    aiTagged: bool | None

    # noinspection StrFormat
    def get_string(self, verbosity=0):
        if verbosity <= 2:
            return self.verbose_level[verbosity].format(**self.model_dump())
        else:
            return self.json()

    def print(self, verbosity=0):
        print(self.get_string(verbosity))

    @model_validator(mode='before')
    def _remove_pinned_by_if_empty(cls, values):
        if not isinstance(values, dict):
            return values
        if values.get('pinnedBy') is None:
            values['pinnedBy'] = []
        elif 'pinnedBy' not in values:
            values['pinnedBy'] = None
        return values


class NewLink(BaseModel):
    """
    API Has different fields for creating a new link
    """
    name: str | None = Field(None, max_length=2048)
    url: str | None = Field(None, max_length=2048)
    type: LinkType | None
    description: str | None = Field(None, max_length=2048)
    tags: List[Tag] | None
    collection: Collection | dict = {}


ALL_MODELS = get_all_subclasses(BaseModel)
