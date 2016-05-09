#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*- 

import re

class StopWords:
    def __init__(self):
        self.cite_pattern = r"[0-9]"
        self.jaswlist = [
            u"・",
            u"％",
            u"あっ",
            u"いる",
            u"%",
            u"▼",
            u"｡",
            u"、",
            u"＠",
            u"#",
            u"$",
            u"&",
            u"'",
            u"\"",
            u"!",
            u"?",
            u"<",
            u">",
            u"\\",
            u"[",
            u"]",
            u"{",
            u"}",
            u"(",
            u")",
            u"「",
            u"」",
            u"『",
            u"』",
            u"gt;(",
            u"｣(",
            u"%｡▼",
            u")▼",
            u"-",
            u"=",
            u"-",
            u"+",
            u"*",
            u"|",
            u"~",
            u"`",
            u".",
            u",",
            u""
        ]

    def remove_mark(self, s):
        marks = [u"-", u"%", u"▼", u"｡", u"、", u"＠", u"#", u"$", u"&", u"'", u"\"", u"!", u"?", u"<", u">", u"\\", u"[", u"]", u"{", u"}", u"(", u")", u"「", u"」", u"『", u"』"]
        for m in marks:
            if s.find(m) >= 0:
                s.replace(m, " ")
        return s 

    def is_stop_word(self, w):
        w = self.remove_mark(w)
        if w in self.jaswlist or re.match(u"[ぁ-ゞ０-９0-9]", w):
            return True
        match = re.search(self.cite_pattern , w)
        if match:
            return True
        else:
            return False
