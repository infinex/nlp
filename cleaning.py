"""
__file__

    cleaning.py.py

__description__

    This file provide function to clean the clean for nlp task
    https://github.com/ChenglongChen/Kaggle_HomeDepot/blob/master/Code/Chenglong/data_processor.py

__author__

    Liang yongjie 

"""

from nltk.stem import WordNetLemmatizer, PorterStemmer
import multiprocessing
import nltk
from bs4 import BeautifulSoup
import nltk
import regex
import csv
import constants_colors

st = PorterStemmer()


def stem_tokens(tokens, stemmer=st):
    """

        Args:
            tokens (list) :
            stemmer (nltk stemmer) : nltk.stem.PorterStemmer()

        Returns:
            list: stem tokens

        Examples:

        import nltk
        english_stemmer = nltk.stem.PorterStemmer()
        stem_tokens(['apples'],english_stemmer)
        #['appl']
    """

    stemmed = []
    for token in tokens:
        stemmed.append(stemmer.stem(token))
    return stemmed


wl = WordNetLemmatizer()


def _tokenize_chinese_chars(text):
    """Adds whitespace around any CJK character."""
    output = []
    for char in text:
        cp = ord(char)
        if self._is_chinese_char(cp):
            output.append(" ")
            output.append(char)
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)


def _is_chinese_char(cp):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True

    return False


def lement_tokens(tokens):
    stemmed = []
    for token in tokens:
        stemmed.append(wl.lemmatize(token))
    return stemmed

  def _clean_text(text):
    """Performs invalid character removal and whitespace cleanup on text."""
    output = []
    for char in text:
      cp = ord(char)
      if cp == 0 or cp == 0xfffd or _is_control(char):
        continue
      if _is_whitespace(char):
        output.append(" ")
      else:
        output.append(char)
    return "".join(output)




"""
--------------------------- Processor ---------------------------
base class
Most of the processings can be casted into the "pattern-replace" framework
"""
class BaseReplacer:
    def __init__(self, pattern_replace_pair_list=[]):
        self.pattern_replace_pair_list = pattern_replace_pair_list

    def transform(self, text):
        for pattern, replace in self.pattern_replace_pair_list:
            try:
                text = regex.sub(pattern, replace, text)
            except:
                pass
        return regex.sub(r"\s+", " ", text).strip()


"""deal with case"""
class LowerCaseConverter(BaseReplacer):
    """
    Traditional -> traditional
    """

    def transform(self, text):
        return text.lower()


class LowerUpperCaseSplitter(BaseReplacer):
    """
    homeBASICS Traditional Real Wood -> homeBASICS Traditional Real Wood
    hidden from viewDurable rich finishLimited lifetime warrantyEncapsulated panels ->
    hidden from view Durable rich finish limited lifetime warranty Encapsulated panels
    Dickies quality has been built into every product.Excellent visibilityDurable ->
    Dickies quality has been built into every product Excellent visibility Durable
    BAD CASE:
    shadeMature height: 36 in. - 48 in.Mature width
    minutesCovers up to 120 sq. ft.Cleans up
    PUT one UnitConverter before LowerUpperCaseSplitter
    Reference:
    https://www.kaggle.com/c/home-depot-product-search-relevance/forums/t/18472/typos-in-the-product-descriptions
    """

    def __init__(self):
        self.pattern_replace_pair_list = [
            (r"(\w)[\.?!]([A-Z])", r"\1 \2"),
            (r"(?<=( ))([a-z]+)([A-Z]+)", r"\2 \3"),
        ]


""" deal with word replacement"""
# 1st solution in CrowdFlower
class WordReplacer(BaseReplacer):
    def __init__(self, replace_fname):
        self.replace_fname = replace_fname
        self.pattern_replace_pair_list = []
        for line in csv.reader(open(self.replace_fname)):
            if len(line) == 1 and line[0].startswith("#"):
                continue
            try:
                pattern = r"(?<=\W|^)%s(?=\W|$)" % line[0]
                replace = line[1]
                self.pattern_replace_pair_list.append((pattern, replace))
            except:
                print(line)
                pass


""" deal with letters"""
class LetterLetterSplitter(BaseReplacer):
    """
    For letter and letter
    /:
    Cleaner/Conditioner -> Cleaner Conditioner
    -:
    Vinyl-Leather-Rubber -> Vinyl Leather Rubber
    For digit and digit, we keep it as we will generate some features via math operations,
    such as approximate height/width/area etc.
    /:
    3/4 -> 3/4
    -:
    1-1/4 -> 1-1/4
    """

    def __init__(self):
        self.pattern_replace_pair_list = [
            (r"([a-zA-Z]+)[/\-]([a-zA-Z]+)", r"\1 \2"),
        ]


""" deal with digits and numbers"""
class DigitLetterSplitter(BaseReplacer):
    """
    x:
    1x1x1x1x1 -> 1 x 1 x 1 x 1 x 1
    19.875x31.5x1 -> 19.875 x 31.5 x 1
    -:
    1-Gang -> 1 Gang
    48-Light -> 48 Light
    .:
    includes a tile flange to further simplify installation.60 in. L x 36 in. W x 20 in. ->
    includes a tile flange to further simplify installation. 60 in. L x 36 in. W x 20 in.
    """

    def __init__(self):
        self.pattern_replace_pair_list = [
            (r"(\d+)[\.\-]*([a-zA-Z]+)", r"\1 \2"),
            (r"([a-zA-Z]+)[\.\-]*(\d+)", r"\1 \2"),
        ]


class DigitCommaDigitMerger(BaseReplacer):
    """
    1,000,000 -> 1000000
    """

    def __init__(self):
        self.pattern_replace_pair_list = [
            (r"(?<=\d+),(?=000)", r""),
        ]


class NumberDigitMapper(BaseReplacer):
    """
    one -> 1
    two -> 2
    """

    def __init__(self):
        numbers = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
            "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
        ]
        digits = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90
        ]
        self.pattern_replace_pair_list = [
            (r"(?<=\W|^)%s(?=\W|$)" % n, str(d)) for n, d in zip(numbers, digits)
        ]


""" deal with unit"""
class UnitConverter(BaseReplacer):
    """
    shadeMature height: 36 in. - 48 in.Mature width
    PUT one UnitConverter before LowerUpperCaseSplitter
    """

    def __init__(self):
        self.pattern_replace_pair_list = [
            (r"([0-9]+)( *)(inches|inch|in|in.|')\.?", r"\1 in. "),
            (r"([0-9]+)( *)(pounds|pound|lbs|lb|lb.)\.?", r"\1 lb. "),
            (r"([0-9]+)( *)(foot|feet|ft|ft.|'')\.?", r"\1 ft. "),
            (r"([0-9]+)( *)(square|sq|sq.) ?\.?(inches|inch|in|in.|')\.?", r"\1 sq.in. "),
            (r"([0-9]+)( *)(square|sq|sq.) ?\.?(feet|foot|ft|ft.|'')\.?", r"\1 sq.ft. "),
            (r"([0-9]+)( *)(cubic|cu|cu.) ?\.?(inches|inch|in|in.|')\.?", r"\1 cu.in. "),
            (r"([0-9]+)( *)(cubic|cu|cu.) ?\.?(feet|foot|ft|ft.|'')\.?", r"\1 cu.ft. "),
            (r"([0-9]+)( *)(gallons|gallon|gal)\.?", r"\1 gal. "),
            (r"([0-9]+)( *)(ounces|ounce|oz)\.?", r"\1 oz. "),
            (r"([0-9]+)( *)(centimeters|cm)\.?", r"\1 cm. "),
            (r"([0-9]+)( *)(milimeters|mm)\.?", r"\1 mm. "),
            (r"([0-9]+)( *)(minutes|minute)\.?", r"\1 min. "),
            (r"([0-9]+)( *)(°|degrees|degree)\.?", r"\1 deg. "),
            (r"([0-9]+)( *)(v|volts|volt)\.?", r"\1 volt. "),
            (r"([0-9]+)( *)(wattage|watts|watt)\.?", r"\1 watt. "),
            (r"([0-9]+)( *)(amperes|ampere|amps|amp)\.?", r"\1 amp. "),
            (r"([0-9]+)( *)(qquart|quart)\.?", r"\1 qt. "),
            (r"([0-9]+)( *)(hours|hour|hrs.)\.?", r"\1 hr "),
            (r"([0-9]+)( *)(gallons per minute|gallon per minute|gal per minute|gallons/min.|gallons/min)\.?",
             r"\1 gal. per min. "),
            (r"([0-9]+)( *)(gallons per hour|gallon per hour|gal per hour|gallons/hour|gallons/hr)\.?",
             r"\1 gal. per hr "),
        ]


""" deal with html tags"""
class HtmlCleaner:
    def __init__(self, parser):
        self.parser = parser

    def transform(self, text):
        bs = BeautifulSoup(text, self.parser)
        text = bs.get_text(separator=" ")
        return text


""" deal with some special characters"""

class QuartetCleaner(BaseReplacer):
    def __init__(self):
        self.pattern_replace_pair_list = [
            (r"<.+?>", r""),
            # html codes
            (r"&nbsp;", r" "),
            (r"&amp;", r"&"),
            (r"&#39;", r"'"),
            (r"/>/Agt/>", r""),
            (r"</a<gt/", r""),
            (r"gt/>", r""),
            (r"/>", r""),
            (r"<br", r""),
            # do not remove [".", "/", "-", "%"] as they are useful in numbers, e.g., 1.97, 1-1/2, 10%, etc.
            (r"[ &<>)(_,;:!?\+^~@#\$]+", r" "),
            ("'s\\b", r""),
            (r"[']+", r""),
            (r"[\"]+", r""),
        ]


""" lemmatizing for using pretrained word2vec model"""

class Lemmatizer:
    def __init__(self):
        self.Tokenizer = nltk.tokenize.TreebankWordTokenizer()
        self.Lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    def transform(self, text):
        tokens = [self.Lemmatizer.lemmatize(token) for token in self.Tokenizer.tokenize(text)]
        return " ".join(tokens)


""" stemming"""
class Stemmer:
    def __init__(self, stemmer_type="snowball"):
        self.stemmer_type = stemmer_type
        if self.stemmer_type == "porter":
            self.stemmer = nltk.stem.PorterStemmer()
        elif self.stemmer_type == "snowball":
            self.stemmer = nltk.stem.SnowballStemmer("english")

    def transform(self, text):
        tokens = [self.stemmer.stem(token) for token in text.split(" ")]
        return " ".join(tokens)


# ----------------------- Processor Wrapper -----------------------
class ProcessorWrapper:
    def __init__(self, processor):
        self.processor = processor

    def transform(self, input):
        if isinstance(input, str):
            out = self.processor.transform(input)
        elif isinstance(input, float) or isinstance(input, int):
            out = self.processor.transform(str(input))
        elif isinstance(input, list):
            # take care when the input is a list
            # currently for a list of attributes
            out = [0] * len(input)
            for i in range(len(input)):
                out[i] = ProcessorWrapper(self.processor).transform(input[i])
        else:
            raise (ValueError("Currently not support type: %s" % type(input).__name__))
        return out


# ------------------- List/DataFrame Processor Wrapper -------------------
class ListProcessor:
    """
    WARNING: This class will operate on the original input list itself
    """

    def __init__(self, processors):
        self.processors = processors

    def process(self, lst):
        for i in range(len(lst)):
            for processor in self.processors:
                lst[i] = ProcessorWrapper(processor).transform(lst[i])
        return lst


class DataFrameProcessor:
    """
    WARNING: This class will operate on the original input dataframe itself
    """

    def __init__(self, processors):
        self.processors = processors

    def process(self, df):
        for processor in self.processors:
            df = df.apply(ProcessorWrapper(processor).transform)
        return df


class DataFrameParallelProcessor:
    """
    WARNING: This class will operate on the original input dataframe itself
    https://stackoverflow.com/questions/26520781/multiprocessing-pool-whats-the-difference-between-map-async-and-imap
    """

    def __init__(self, processors, n_jobs=4):
        self.processors = processors
        self.n_jobs = n_jobs

    def process(self, dfAll, columns):
        df_processor = DataFrameProcessor(self.processors)
        p = multiprocessing.Pool(self.n_jobs)
        dfs = p.imap(df_processor.process, [dfAll[col] for col in columns])
        for col, df in zip(columns, dfs):
            dfAll[col] = df
        return dfAll


COLOR_LIST = [x.lower() for x in constants_colors.COLOR_TO_HEX_DICT.keys()]
COLORS_PATTERN = r"(?<=\W|^)%s(?=\W|$)" % ("|".join(COLOR_LIST))
UNITS = [" ".join(r.strip().split(" ")[1:]) for p, r in UnitConverter().pattern_replace_pair_list]
UNITS_PATTERN = r"(?:\d+[?:.,]?\d*)(?: %s\.*)?" % ("|".join(UNITS))
DIM_PATTERN_NxNxN = r"%s ?x %s ?x %s" % (UNITS_PATTERN, UNITS_PATTERN, UNITS_PATTERN)
DIM_PATTERN_NxN = r"%s ?x %s" % (UNITS_PATTERN, UNITS_PATTERN)
