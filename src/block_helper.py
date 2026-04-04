# takes 1st 7 char(s) as input and check if eliginble heading
# Headings start with 1-6 # characters, followed by a space and then the heading text.
def is_heading(text):
    length = 7
    if len(text) <= length:
        return False
    i = 0
    for ch in text:
        if ch != "#":
            break
        i += 1
    return i <= len(text)-1 and i < length and text[i] == " "

# Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks
def is_code_block(text):
    return len(text) >= 7 and text[:4] == "```\n" and text[-3:] == "```"

def is_quote(text):
    lines = text.split("\n")
    for line in lines:
        if line and not line.startswith(">"):
            return False
    return True

def is_ulist(text):
    lines = text.split("\n")
    for line in lines:
        if line and not line.startswith("- "):
            return False
    return True

def is_olist(text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line and not line.startswith(f"{i+1}. "):
            return False
    return True