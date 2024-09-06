from enum import Enum


from enum import Enum

class Language(str, Enum):
    chinese_cantonese = "zh-yue"
    english = "en"
    arabic = "ar"
    bengali = "bn"
    czech = "cs"
    danish = "da"
    german = "de"
    greek = "el"
    spanish = "es"
    estonian = "et"
    farsi = "fa"
    finnish = "fi"
    french = "fr"
    hebrew = "he"
    hindi = "hi"
    croatian = "hr"
    hungarian = "hu"
    indonesian = "id"
    italian = "it"
    japanese = "ja"
    korean = "ko"
    lithuanian = "lt"
    latvian = "lv"
    macedonian = "mk"
    dutch = "nl"
    norwegian = "no"
    polish = "pl"
    portuguese = "pt"
    romanian = "ro"
    russian = "ru"
    slovak = "sk"
    slovenian = "sl"
    albanian = "sq"
    serbian = "sr"
    swedish = "sv"
    thai = "th"
    turkish = "tr"
    ukrainian = "uk"
    urdu = "ur"
    vietnamese = "vi"
    chinese_simplified = "zh-cn"
    chinese_traditional = "zh-tw"



class RagMethod(str, Enum):
    DirectMatch = "DirectMatch"
    ParentDoc = "ParentDoc"
    NER = "NER"
    Hypothetical = "HypoQuery"


class RagType(str, Enum):
    Common = "Common"
    Fusion = "Fusion"

    