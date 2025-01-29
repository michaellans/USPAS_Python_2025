import re
import pandas as pd

##String Handling
#strings have indices which indicates specific characters.
txt = "Hello World!"
print(txt[0])
print(txt[6])

#The find method returns the first instance of a character
txt = "Hello World! What would you like to do today?"
dex = txt.find('W')
print(dex)
print(txt[dex:(dex+5)])
#and find is case-sensitive
dex = txt.find('w')
print(txt[dex:(dex+5)])

#The split methods creates a list delimited by the split string.
txt = "Hello World! What would you like to do today?"
stxt = txt.split('!')
print(stxt)
print(stxt[0])
print(stxt[1])
#notice the '!' character does not appear in either part.

#split can create longer lists with more delimiters.
txt = "1 baa 2 baa 3 baa 4 baa 5"
stxt = txt.split(' baa ')
for lp in range(len(stxt)):
  print(10*int(stxt[lp]))

##Regular Expressions
#Regular expressions allow for much more elaborate search criteria
#split is still available as a re method
#+ means one or more of the preceeding character
#* means zero or more of the preceeding character
txt = "1 ba 2 baa 3 baaa 4 baaaa 5"
stxt = re.split(r"ba+",txt)
print(stxt)
#\s is an escape character for a space.
stxt = re.split(r"\s",txt)
print(stxt)

#in place of find, re uses search.start and search.end
#\d means any numerical digit
#\. is an escape character for .
#? means zero or one preceeding character.
txt = "pi is approximately 3.14159, if you want more digits than just 3 or 3.14."
#look for an integer or decimal number
m_obj = re.search(r"\d\.?\d*",txt)
print(m_obj.group())
print(m_obj.start())
print(m_obj.end())
print(txt[m_obj.start():m_obj.end()])

#findall shows all strings that match
#[] means any one of the characters in the bracket
txt = "pi is approximately 3.14159, if you want more digits than just 3 or 3.14."
ftxt = re.findall(r"[0-9]\.?[0-9]*",txt)
print(ftxt)


#More examples
#. matches any character
txt = "pi is approximately 3.14159, if you want more digits than just 3 or 3.14."
print(re.findall(r"y.u",txt))
#if there is ambiguity, it will find the longer matche
print(re.findall(r"p.*y",txt))

#[] means any one of the characters in the bracket
#{2} means exactly 2 of something
txt = "Would you look at protein yield of the boiled egg?"
print(re.findall(r"[aeiou]{2}",txt))

#\b means beginning of a word (boundary of alphanumeric and otherwise)
print(re.findall(r"\b.[aeiou]{2}",txt))

#\w means any alphanumeric
#this expression will find the full word with the double vowel.
print(re.findall(r"\w*[aeiou]{2}\w*",txt))

#| means either
txt = "Would you look at protein yield of the boiled egg?"
print(re.findall(r".ou|.gg",txt))

#[^yW] means any character except y or W
txt = "Would you look at protein yield of the boiled egg?"
print(re.findall(r".[aeiou]{2}",txt))
print(re.findall(r"[^yW][aeiou]{2}",txt))


#regular expression can also be used with pandas
#load a simple pandas dataframe
df = pd.DataFrame({'Text': ['eggs', 'milk', 'oats'], 'Cost': [6.20, 3.70, 0.70]})
print(df)
print(df.columns)
print(df.iloc[0])

#find the rows with gg or oa in Text
dex = df['Text'].str.contains(r"gg|oa", regex=True)
print(dex)
#find the corresponding costs values for those rows
print(df['Cost'][dex])
#sum the corresponding cost calues for those rows
print(df['Cost'][dex].sum())
