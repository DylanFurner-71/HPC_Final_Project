#!/usr/bin/env python


import string


# first two functions take line by line input
# last two functions take whole text input
def find_title(text):
    if "Title: " in text:
        title = text[text.index("Title: ")+len("Title: "):]
        title2 = "_".join(title)
        return title2
    if "title: " in text:
        title = text[text.index("title: ") + len("title: "):]
        title2 = "_".join(title)
        return title2

    else:
        return ""


def find_author(text):
    if "Author: " in text or "author: " in text or "written by: " in text:
        title = text.split(' ')[1:]
        title2 = "_".join(title)
        return title2
    else:
        return ""


def check_specific_start(curr_string, text, text2, in_string):
    if curr_string in text2:
        text = text[
               text2.index(curr_string)
               + len(curr_string):]
        text2 = text.lower()
        in_string = True
    return text, text2, in_string

def check_start_of_text(text, in_string):
    text2 = text
    text2.lower()
    if not in_string:
        text, text2, in_string = check_specific_start("to header material", text, text2, in_string)
        text, text2, in_string = check_specific_start("the project gutenberg etext", text, text2, in_string)
        text, text2, in_string = check_specific_start("start of the project gutenberg ebook", text, text2, in_string)
        text, text2, in_string = check_specific_start("start of this project gutenberg ebook", text, text2, in_string)

    return text[text.lower().index(text2):], in_string

def clean_start_of_text(text, title, author):
    text2 = "".join([s for s in text.splitlines(True) if s.strip("\r\n")])
    text2 = text2.lower()
    curr_string = "translated by " + author.replace("_", " ")
    if curr_string in text2:
        text = text[
               text2.index(curr_string)
               + len(curr_string):]
        text2 = text.lower()
    curr_string = "Translated by " + author.replace("_", " ")
    if curr_string in text2:
        text = text[
               text2.index(curr_string)
               + len(curr_string):]
        text2 = text.lower()
    curr_string = "by " + author.replace("_", " ")
    if curr_string in text2[0:len(curr_string) * 20]:
        text = text[
               text2.index(curr_string)
               + len(curr_string):]
        text2 = text.lower()
    curr_string = "by " + author.split("_")[0]
    if curr_string in text2[0:len(curr_string) * 15]:
        text = text[
               text2.index(curr_string)
               + len(curr_string):]
        text2 = text.lower()
    curr_string = author.split("_")[0]
    if curr_string in text2[0:len(curr_string) * 15]:
        text = text[
               text2.index(curr_string)
               + len(curr_string):]
        text2 = text.lower()
    if len(author.split("_")) > 1:
        curr_string = author.split("_")[1]
        if curr_string in text2[0:len(curr_string) * 15]:
            text = text[text2.index(curr_string)
                        + len(curr_string):]
            text2 = text.lower()
    curr_string = "contents"
    if curr_string in text2[0:len(curr_string) * 15]:
        text = text[
               text2.index(curr_string)
               + len(curr_string):]
        text2 = text.lower()
    curr_string = author.replace("_", " ")
    if curr_string in text2[0:len(curr_string) * 15]:
        text = text[text2.index(curr_string) + len(curr_string):]
        text2 = text.lower()
    curr_string = title
    if curr_string in text2[0:len(curr_string) * 15]:
        text = text[text2.index(curr_string) + len(curr_string):]
        text2 = text.lower()
    if "lincoln's gettysburg address, given november 19, 1863" in text2:
        text = text[text.index("lincoln's gettysburg address, given november 19, 1863"):]
    return text


def clean_end_of_text(text1, in_string):  #takes in a line of text, boolean originally meant to be false from parent function call
    if "end of the project gutenberg ebook" in text1:
        text1 = text1[:text1.index("end of the project gutenberg ebook")]
        in_string = True
    if "end of this project gutenberg ebook" in text1:
        text1 = text1[:text1.index("end of this project gutenberg ebook")]
        in_string = True
    if "end of the collected etexts" in text1:
        text1 = text1[:text1.index("end of the collected etexts")]
        in_string = True
    return text1, in_string

