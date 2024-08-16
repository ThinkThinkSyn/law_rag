from enum import Enum


class Language(str, Enum):
    english = "en"
    chinese = "zh"


class RagMethod(str, Enum):
    DirectMatch = "DirectMatch"
    ParentDoc = "ParentDoc"
    NER = "NER"
    Hypothetical = "HypoQuery"


class RagType(str, Enum):
    Common = "Common"
    Fusion = "Fusion"

    