#!/usr/bin/env python3
#-*-coding:utf-8-*-
# mp3 player

'''
version: window 1.0 version
release: 2017.10.06
'''

from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk
from mutagen.id3 import ID3, USLT, TRCK, TIT2, TPE1, TALB, TDRC, TCON, TENC, COMM, APIC, error
from mutagen import File
import vlc
import os
import random
import timeit
import time
import threading
import sys

# set env variable for vlc module
os.environ["VLC_PLUGIN_PATH"] = "/usr/lib/vlc/plugins/"

class Song:
	'''
	get song info.
	'''

	def __init__(self, song_name):
		self.song_name = song_name

	def get_metadata(self):
		global art_name
		global info

		mp3 = File(self.song_name)

		meta = {}
		art_name = "music.png"
		duration = mp3.info.length
		pTimeMin = str(int(duration // 60))
		pTimeSec = str(int(duration % 60))

		if int(pTimeMin) < 10:
			pTimeMin = "0" + pTimeMin

		if int(pTimeSec) < 10:
			pTimeSec = "0" + pTimeSec

		meta["재생시간"] = str(" : ".join([pTimeMin, pTimeSec]))
		try:
			meta["가사"] = str(mp3.tags.getall("USLT")[0])
		except:
			meta["가사"] = ""

		for key in mp3.tags:
			if key == "APIC:Cover" or key == "APIC:":
				art_name = os.path.splitext(self.song_name)[0] + ".jpg"
				artwork = mp3.tags[key].data
				if not os.path.isfile(art_name):
					with open(art_name, 'wb') as img:
					   img.write(artwork)
				else:
					print("앨범 아트가 이미 존재합니다.")

			if key == "TALB":
				meta["앨범"] = str(mp3.tags[key])					

			if key == "TIT2":
				meta["타이틀"] = str(mp3.tags[key])
				
			if key == "TPE1":
				meta["가수"] = str(mp3.tags[key])	

			if key == "TCON":
				meta["장르"] = str(mp3.tags[key])
			
			if key == "TDRC":
				date = str(mp3.tags[key])
				date = ".".join([date[:4] , date[4:6], date[6:8]])
				meta["발매일"] = date

		# concatenate song info 
		info = ""
		for key in sorted(meta.keys()):
			info += " : ".join([key, meta[key]])
			info += "\n------------------------------\n"

		return duration, len(meta["가사"])

class Play:
	'''
	control music playing
	'''

	def __init__(self):
		self.dir = 0
		self.p = None
		self.t = None

	def get_songs_list(self):
		cur_dir = os.getcwd()

		print("---------------- [track] ----------------")
		for file in os.listdir(cur_dir):
			for e in ext:
				if os.path.splitext(file)[1][1:] == e:
					songs_track.append(file)
					print(file)
					break		
		print("-----------------------------------------")

		# current directory -> play list
		play_list.delete(0, "end")
		for song in songs_track:
			play_list.insert("end", song)

	def load_track(self):  
		self.line = 0
		idx, filename = find_song(pos)
		song = Song(filename)	
		self.duration, self.len_letters = song.get_metadata()
		self.p = vlc.MediaPlayer(filename)

	def playing(self):
		if self.p: print(self.p.get_state())
		
		if isEnded:
			if self.p: self.p.stop()
			if self.t: self.t.cancel()
		else:
			if self.p and str(self.p.get_state()) == "State.Ended":
				self.t.cancel()
				self.next_song()
				self.play_music()
			else:
				self.t = threading.Timer(2, self.playing)
				self.t.start()

	def play_music(self):
		if self.p: self.p.play()
		p_btn.configure(text="Pause", command=self.pause_music)
		self.playing()

	def pause_music(self):
		if self.p: self.p.pause()
		p_btn.configure(text="Play", command=self.play_music)
	
	def ch_img(self):
		global img_copy
		print("art name : {}".format(art_name))
		# idx, filename = find_song(pos)
		# img_path = os.path.splitext(filename)[0] + ".jpg"
		img = Image.open(art_name).resize((width, height))
		photo = ImageTk.PhotoImage(img)
		img_copy = img.copy()

		album_cover.configure(image=photo)
		album_cover.image = photo

	def ch_focus(self):
		# enable focus
		play_list.selection_set(pos)
		play_list.activate(pos)

	def ch_song(self):
		if self.p: self.p.stop()
		self.load_track()
		self.ch_img()
		self.ch_focus()
		p_btn.configure(text="Play", command=self.play_music)
		song_info.delete('1.0', END)
		song_info.insert("1.0", info)
		song_info.tag_add("center", "1.0", "end")

	def prev_song(self):
		self.dir = -1
		self.ch_dir()
		
	def next_song(self):
		self.dir = 1
		self.ch_dir()

	# problem
	def ch_dir(self):
		if search_size != 0:
			global pos
			play_list.selection_clear(pos)
			pos = (pos + self.dir) % search_size
			self.ch_song()
			print(play_list.get(pos))
			# scroll up or down
			play_list.see(pos)
		else:
			print("no songs...")
		

# callback for user events
def ch_bg_night(self):
	song_info.configure(fg="orange")

def ch_bg_day(self):
	song_info.configure(fg="#383a39")

def resize(e):
	img = img_copy.resize((e.width, e.width))
	photo = ImageTk.PhotoImage(img)
	album_cover.configure(image=photo)
	album_cover.image = photo

def show_list(e):
	time.sleep(0.1)
	song_info.pack_forget()
	play_list.pack(fill=BOTH, expand=True)

	print("double clicked !!")
	# print(play_list.get(0, END))

def show_info(e):
	time.sleep(0.1)
	play_list.pack_forget()
	song_info.pack()
	print("show info")
	

def find_song(needle):
	f_song = play_list.get(needle)

	for i, f_name in enumerate(songs_track):
		song = os.path.basename(f_name)
		if song == f_song: 
			break

	return i, f_name

def click_song(e):
	global pos
	play_list.selection_clear(pos)
	pos = play_list.nearest(e.y)
	play.ch_song()
	print(pos)
	print("clicked song : {}".format(play_list.get(pos)))

def remove_song(e):
	global pos
	del_idx = play_list.nearest(e.y)
	idx, filename = find_song(del_idx)
	play_list.delete(del_idx)
	print("{}이 삭제되었습니다.".format(songs_track[idx]))
	del songs_track[idx]

	if pos > del_idx:
		pos = pos -1
	elif pos == del_idx:
		play.ch_song()

def scrolldown_list(e):
	time.sleep(0.2)
	play.next_song()	

def search_songs(key):
	global search_size
	global pos 
	sub_str = key.char
	searched_songs = []
	for file_name in songs_track:
		song = os.path.basename(file_name)
		if sub_str.lower() in song.lower():
			searched_songs.append(song)
	
	play_list.delete(0, "end")
	if searched_songs:
		for song in searched_songs:
			play_list.insert("end", song)
			print(song)
		search_size = len(searched_songs)
	else:
		for file_name in songs_track:
			song = os.path.basename(file_name)
			play_list.insert("end", song)
		search_size = len(songs_track)
		print("not searched !!")
	pos = 0

def add_songs():
	global search_size
	file_names = askopenfilenames()

	#check if file is valid
	for file_name in file_names:
		song = os.path.basename(file_name)
		for e in ext:
			if os.path.splitext(song)[1][1:] == e:
				play_list.insert("end", song)
				songs_track.append(file_name)
				search_size += 1
				break

	print("size : {}".format(search_size))
	print("open")

# terminate timer and music
def on_closing():
	global isEnded
	isEnded = True
	print("program closed...")
	window.destroy()


# set album size
width = 500
height = 500
isEnded = False
bg_color = "#95E0C8"

ext = ['mp3', 'flac']
songs_track = []
art_name = "music.png" 
info = "Double click to view songs list !!"
pos = 0
search_size = 0

# create GUI to control songs
window = Tk()
window.title("Sylee Music Player")
window.geometry("500x800")
# window.resizable(0, 0) # do not resize
window.minsize(450,700) 
window.maxsize(700,900)
window.attributes("-alpha", 0.95)
window.config(bg=bg_color)

# create playing control instance
play = Play()

play_list = Listbox(window, bg="black", fg="#383a39", font=("굴림체", 12, "bold"), borderwidth=0,
                    highlightthickness=0, activestyle=NONE, selectbackground="orange", selectforeground="#F0F0D0")
play_list.bind('<Double-Button-1>', click_song)
play_list.bind("<B1-Motion>", show_info)
play_list.bind("<B3-Motion>", scrolldown_list)
play_list.bind("<Double-Button-3>", remove_song)

# get list from current directory
# play.get_songs_list()
# pos = random.randint(0, play_list.size()-1)
# play.load_track()

# add album cover to label
img = Image.open(art_name).resize((width, height))
photo = ImageTk.PhotoImage(img)
img_copy = img.copy()

album_cover = Label(window, image=photo)
album_cover.pack(fill=BOTH, expand=True)
album_cover.bind('<Configure>', resize)

# control buttons
btn_frame = Frame(bg=bg_color)
btn_frame.pack(fill="none", expand=True, pady=5)

prev_btn = Button(btn_frame, text="Prev", fg="ivory2", bg="#383a39", font="Verdana 10 bold", command=play.prev_song)
prev_btn.pack(side=LEFT, padx=5, pady=5)

p_btn = Button(btn_frame, text="Play", fg="mint cream", bg="#383a39", font="Verdana 10 bold", command=play.play_music)
p_btn.pack(side=LEFT, padx=5, pady=5)

next_btn = Button(btn_frame, text="Next", fg="ivory2", bg="#383a39", font="Verdana 10 bold", command=play.next_song)
next_btn.pack(side=LEFT, padx=5, pady=5)

add_btn = Button(btn_frame, text="Add", fg="ivory2", bg="#383a39", font="Verdana 10 bold", command=add_songs)
add_btn.pack(side=LEFT, padx=5, pady=5)

search_frame = Frame(bg=bg_color)
search_frame.pack(fill="none", expand=True, pady=5)

# search bar
search = Entry(search_frame, borderwidth=0, highlightthickness=0, width=20, font=("굴림체", 12, "bold"))
search.pack(side=LEFT, padx=5, pady=5)
search.bind("<Key>", search_songs)

# search icon
img2 = Image.open("search.png").resize((20, 20))
photo2 = ImageTk.PhotoImage(img2)
search_icon = Label(search_frame, image=photo2, bg=bg_color)
search_icon.pack(side=LEFT, padx=5, pady=5)

# display info.
song_info = Text(window, wrap=None, bg="black", fg="#383a39", font=("굴림체", 12, "bold"), borderwidth=0, highlightthickness=0, pady=15)
song_info.tag_configure("center", justify='center')
song_info.insert("1.0", info)
song_info.tag_add("center", "1.0", "end")
song_info.pack()
song_info.bind('<Double-Button-1>', show_list)
song_info.bind("<Enter>", ch_bg_night)
song_info.bind("<Leave>", ch_bg_day)

window.protocol("WM_DELETE_WINDOW", on_closing)

# process events
window.mainloop()


