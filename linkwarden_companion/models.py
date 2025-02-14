import pydantic
import datetime

from enum import Enum
from typing import List
from pydantic import AfterValidator, Field
from linkwarden_companion.utils import get_all_subclasses


class LinkType(str, Enum):
    """
    Enum for link types
    """
    URL = 'url'
    PDF = 'pdf'
    IMAGE = 'image'


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
    id: int
    name: str
    type: str
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
    pinnedBy: List[int]


class NewLink(BaseModel):
    """
    API Has different fields for creating a new link
    """
    name: str | None = Field(None, max_length=2048)
    url: str | None = Field(None, max_length=2048)
    type: LinkType | None
    description: str | None = Field(None, max_length=2048)
    tags: List[Tag] | None
    collection: Collection | None


ALL_MODELS = get_all_subclasses(BaseModel)
