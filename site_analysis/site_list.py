from typing import TypeVar, Generic, List
from .site import Site
from collections import Sequence

T = TypeVar('T')

class SiteList(List[Site]):

    def __init__(self) -> None:
        self.sites: List[Site] = []

