from enum import Enum


class Language(str, Enum):
    Chinese_Cantonese = "zh-yue"
    English = "en"
    Arabic = "ar"
    Bengali = "bn"
    Czech = "cs"
    Danish = "da"
    German = "de"
    Greek = "el"
    Spanish = "es"
    Estonian = "et"
    Farsi = "fa"
    Finnish = "fi"
    French = "fr"
    Hebrew = "he"
    Hindi = "hi"
    Croatian = "hr"
    Hungarian = "hu"
    Indonesian = "id"
    Italian = "it"
    Japanese = "ja"
    Korean = "ko"
    Lithuanian = "lt"
    Latvian = "lv"
    Macedonian = "mk"
    Dutch = "nl"
    Norwegian = "no"
    Polish = "pl"
    Portuguese = "pt"
    Romanian = "ro"
    Russian = "ru"
    Slovak = "sk"
    Slovenian = "sl"
    Albanian = "sq"
    Serbian = "sr"
    Swedish = "sv"
    Thai = "th"
    Turkish = "tr"
    Ukrainian = "uk"
    Urdu = "ur"
    Vietnamese = "vi"
    Chinese_Simplified = "zh-cn"
    Chinese_Traditional = "zh-tw"


class RagMethod(str, Enum):
    DirectMatch = "DirectMatch"
    ParentDoc = "ParentDoc"
    NER = "NER"
    Hypothetical = "HypoQuery"


class RagType(str, Enum):
    Common = "Common"
    Fusion = "Fusion"

    