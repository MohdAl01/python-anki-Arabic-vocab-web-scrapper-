
import requests 
import lxml 
from bs4 import BeautifulSoup 
import genanki	
import os
template_index = 1
Arabic_model = genanki.Model(
  1607392318,
  'Arabic_model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': f'Card {template_index}',
      'qfmt': "<div dir=rtl style='text-align: center; font-family: Arial; font-size: 40px; color: white'>{{Question}}</span></div>",
      'afmt': "<div dir=rtl style='text-align: center; font-family: Arial; font-size: 40px; color: white'>{{Question}}</span></div><hr id=answer><div style='text-align: centre; font-family: Arial; font-size: 20px; color:white'>{{Answer}}</span>",
    },
  ])
Arabic_reversed = genanki.Model(
  1346232318,
  'Arabic_model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': f'Card {template_index}',
      'qfmt': "<div style='text-align: centre; font-family: Arial; font-size: 20px; color:white'>{{Question}}</span></div>",
      'afmt': "<div style='text-align: centre; font-family: Arial; font-size: 20px; color:white'>{{Question}}</span></div><hr id=answer><div dir=rtl style='text-align: center; font-family: Arial; font-size: 40px; color: white'>{{Answer}}</span>",
    },
  ])

Arabic_deck = genanki.Deck(
  2059450111,
  'Arabic vocab')
# defines the genanki model and deck

def Arabic_sky_webscrapping(htmlf):
	with open(htmlf, 'rb') as html_file:
		soup = BeautifulSoup(html_file, 'lxml')
		# opens html file, and processes it using lxml 
		vocab_list = []

		words = soup.find_all('tr')
		# scrapes all table rows of the file. the row contains the english word, the MSA arabic translation, 
		# and the Egyptian arabic translation, if there is any
		for i in words:
			
			english_word = i.find('td').text
			arabic_on_row = i.find_all('td', dir='rtl')
			# the english word is always the first element of the row
			# the arabic word(s) always have a right-to-left dir
			
			#vocab_list.append(english_word)
			
			if english_word == "":
				pass
			elif english_word == '\xa0':
				for j in arabic_on_row:
					vocab_list[-1].append(j.text)
			else:
				vocab = []
				vocab.append(english_word)
				for j in arabic_on_row:
					vocab.append(j.text)
				vocab_list.append(vocab)
			# The base case is when there is an english word and two arabic translations (one MSA, one Egyptian) on a row. 
			# In that case, append the english word to the vocab list first. Then append the two arabic translations. 
			# Then append the vocab the vocab_list. admittedly, if I were to do this again, I'd use a dictionary instead of a 
			# list of lists. I've always been more comfortable using 2-d arrays, but using a dictionary would've made the code cleaner.
			
			# If the "english word" is an empty string, than the row is just there for formatting reasons, and there is no actual vocab on the
			# the row. So, in that case, skip the line

			# if the "english word" is '\xa0', a hard space, then the arabic words are synonynms for the english word on the above line
			# So, append the arabic words to the previous list in vocab_list. 
		waste = vocab_list.pop(0)
		# the first list in vocab list is always ['English', 'Standard Arabic', 'Egyptian Arabic']. I dont want this in the anki deck, so I pop it
		combined_vocab_list = []
		for i in vocab_list:
			english_word = i.pop(0)
			arabic_word = ""
			for j in i:
				arabic_word += f"{j}<br>"
			combined_vocab_list.append([arabic_word,english_word])	
	# For the anki deck, I need a front card and back card. Meaning I need a list with the first index being the english word, and 
	# the second being all the arabic words. This for loop goes through the arabic words and combines them, using an f-string, into
	# one string. It then appends the [arabic_word, english_word] to combined_vocab_list 

		return combined_vocab_list
vocab_list = Arabic_sky_webscrapping("animals.html")
x = 0
for filename in os.listdir(r"C:\Users\moham\Desktop\python projects\sort later\html"):

	if filename.endswith(".html"):
		vocab_list = Arabic_sky_webscrapping(filename)

		list_of_5 = []
		list_of_5_reversed = []

		for i in vocab_list:
			my_note = genanki.Note(model=Arabic_model,fields=[i[0], i[1]])
			my_note_reversed = genanki.Note(model=Arabic_reversed,fields=[i[1], i[0]])
			template_index += 1

			if len(list_of_5) < 5:
				list_of_5.append(my_note)
				list_of_5_reversed.append(my_note_reversed)
			else:
				list_of_5.append(my_note)
				list_of_5_reversed.append(my_note_reversed)
				for j in list_of_5:
					Arabic_deck.add_note(j)
				list_of_5 = []
				for k in list_of_5_reversed:
					Arabic_deck.add_note(k)
				list_of_5_reversed = []

		for i in list_of_5:
			Arabic_deck.add_note(i)
		for j in list_of_5_reversed:
			Arabic_deck.add_note(j)
# print(x)
# print(template_index)
genanki.Package(Arabic_deck).write_to_file('output.apkg')

	
			# Arabic_deck.add_note(my_note)
			# Arabic_deck.add_note(my_note_reversed)
