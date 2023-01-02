from tkinter import*
from tkinter.messagebox import*
from tkinter.scrolledtext import*
from tkinter import ttk
from sqlite3 import*
import time
import datetime
import numpy as np
import requests
import bs4
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import pandas as pd

root = Tk()
root.title("S.M.S")
root.geometry("400x400+400+100")


def f1():
	root.withdraw()
	add_st.deiconify()

def f2():
	add_st.withdraw()
	root.deiconify()

def f3():
	root.withdraw()
	view_st.deiconify()
	con = None
	try:
		con = connect("StudentData.db")
		sql = "select * from student"
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		if len(data) != 0:
			view_st_table.delete(*view_st_table.get_children())
		for d in data:
			view_st_table.insert('',END,values = d)
		con.commit()

	except Exception as e:
		showerror("issue" , e)
	
	finally:
		if con != None:
			con.close()

def f4():
	view_st.withdraw()
	root.deiconify()

def f5():
	root.withdraw()
	upd_st.deiconify()

def f6():
	upd_st.withdraw()
	root.deiconify()

def f7():
	root.withdraw()
	del_st.deiconify()

def f8():
	del_st.withdraw()
	root.deiconify()

def f9():
	con = None
	try:
		con = connect("StudentData.db")
		sql = "insert into student values('%s','%s','%s')"
		rno = int(add_st_entrno.get())
		name = add_st_entname.get()
		marks = int(add_st_entmarks.get())
		if marks < 0 or marks > 100:
			showerror("FAILURE","MARKS OUT OF RANGE")
			con.rollback()
		else:
			showinfo("SUCCESS","RECORD ADDED")
			cursor = con.cursor()
			cursor.execute(sql % (rno,name,marks))
			con.commit()

	except Exception as e:
		showerror("FAILURE" , e)

	finally:
		if con != None:
			con.close()
def f10():
	con = None
	try:
		con = connect("StudentData.db")
		sql = "update student set name = '%s',marks = '%s' where rno = '%s'"
		cursor = con.cursor()
		name = upd_st_entname.get()
		marks = int(upd_st_entmarks.get())
		rno = int(upd_st_entrno.get())
		if marks < 0 or marks > 100:
			showerror("FAILURE","MARKS OUT OF RANGE")
			con.rollback()
		else:
			showinfo("SUCCESS","RECORD UPDATED")
			cursor = con.cursor()
			cursor.execute(sql % (name,marks,rno))
			con.commit()

	except Exception as e:
		showerror("FAILURE" , e)

	finally:
		if con != None:
			con.close()

def f11():
	con = None
	try:
		con = connect("StudentData.db")
		sql = "delete from student where rno = '%s'"
		cursor = con.cursor()
		rno = int(del_st_entrno.get())
		cursor.execute(sql % (rno))
		con.commit()
		showinfo("SUCCESS" , "RECORD DELETED")

	except Exception as e:
		showerror("FAILURE" , e)

	finally:
		if con != None:
			con.close()

def f12():
	try:
		web_add = "https://www.brainyquote.com/quote_of_the_day"
		res = requests.get(web_add)

		data = bs4.BeautifulSoup(res.text, "html.parser")
	
		info = data.find('img' , {'class':'p-qotd'})

		quote = info['alt']	
		showinfo("Quote of the day" , quote)

	except Exception as e:
		showerror("issue" , e)

def f13():
	try:
		web_address = "https://ipinfo.io/"
		res = requests.get(web_address)

		data = res.json()

		city_name = data['city']

		loc = data['loc']
		showinfo("LOCATION",city_name)

	except Exception as e:
		showerror("issue", e)

def f14():
	con = None
	con = connect("StudentData.db")
	cursor = con.cursor()
	cursor.execute("select rno, marks from student")
	rno = []
	marks = []
	for row in cursor.fetchall():
		rno.append(row[0])
		marks.append(row[1])

	plt.bar(rno,marks, label = 'STUDENTS')
	plt.xlabel("STUDENT")
	plt.ylabel("MARKS")
	plt.title("STUDENT MARKS")
	plt.legend(shadow=True)
	plt.grid()
	plt.show()

def f15():
	web_add = "https://weather.com/en-IN/weather/today"
	res = requests.get(web_add)
	data = bs4.BeautifulSoup(res.text,"html.parser")
	info = data.find_all('div',{"class":"CurrentConditions--dataWrapperInner--2h2vG"})
	temp = info[0].find('span').text
	showinfo("TEMPERATURE", temp)

btnADD = Button(root, text = 'ADD', width = 10, font=('courier', 18, 'bold'),command=f1)
btnVIEW = Button(root, text = 'VIEW',width = 10, font=('courier',18,'bold'),command=f3)
btnUPDATE = Button(root, text = 'UPDATE',width = 10, font=('courier', 18,'bold'),command=f5)
btnDELETE = Button(root, text = 'DELETE',width = 10,font=('courier',18,'bold'),command=f7)
btnCHARTS = Button(root, text = 'CHARTS',width = 10, font=('courier',18,'bold'),command=f14)


btnADD.pack(pady = 5)
btnVIEW.pack(pady = 5)
btnUPDATE.pack(pady = 5)
btnDELETE.pack(pady = 5)
btnCHARTS.pack(pady = 5)


btnloc = Button(root, text = "LOCATION" , font=('courier',18,'bold'),command=f13)
btntemp = Button(root, text = "TEMPERATURE" , font=('courier',18,'bold'),command=f15)
btnQOTD = Button(root, text = "QOUTE OF THE DAY" , font=('courier',18,'bold'),command=f12)
btnloc.place(x = 5, y = 300)
btntemp.place(x = 200 , y = 300)
btnQOTD.place(x = 5 , y = 350)



add_st = Toplevel(root)
add_st.title("ADD STUDENT")
add_st.geometry("400x400+400+100")

add_st_lblrno = Label(add_st, text= 'ENTER RNO', font=('courier',18,'bold'))
add_st_entrno = Entry(add_st, bd = 5, font=('courier',18,'bold'))
add_st_lblname = Label(add_st, text = 'ENTER NAME',font=('courier',18,'bold'))
add_st_entname = Entry(add_st, bd = 5, font=('courier',18,'bold'))
add_st_lblmarks = Label(add_st, text = 'ENTER MARKS(0-100)',font=('courier',18,'bold'))
add_st_entmarks = Entry(add_st, bd = 5, font=('courier',18,'bold'))
add_st_btnsave = Button(add_st, text = 'SAVE',font=('courier',18,'bold'),command=f9)
add_st_btnback = Button(add_st, text = 'BACK',font=('courier',18,'bold'),command=f2)

add_st_lblrno.pack(pady = 6)
add_st_entrno.pack(pady = 6)
add_st_lblname.pack(pady = 6)
add_st_entname.pack(pady = 6)
add_st_lblmarks.pack(pady = 6)
add_st_entmarks.pack(pady = 6)
add_st_btnsave.pack(pady = 6)
add_st_btnback.pack(pady = 6)
add_st.withdraw()

view_st = Toplevel(root)
view_st.title("VIEW STUDENT")
view_st.geometry("800x600+300+65")

scroll_x = Scrollbar(view_st,orient=HORIZONTAL)
scroll_y = Scrollbar(view_st,orient=VERTICAL)
view_st_btnback = Button(view_st, text='BACK',font=('courier',18,'bold'),command=f4)
view_st_table = ttk.Treeview(view_st ,columns=("rno","name","marks"),xscrollcommand = scroll_x.set,yscrollcommand = scroll_y.set)
scroll_x.pack(side=BOTTOM,fill = X)
scroll_y.pack(side=RIGHT,fill= Y)
scroll_x.config(command=view_st_table.xview)
scroll_y.config(command=view_st_table.yview)
view_st_table.heading("rno",text = "RNO.")
view_st_table.heading("name",text = "NAME")
view_st_table.heading("marks",text = "MARKS")
view_st_table['show']='headings'
view_st_table.column("rno",width=20)
view_st_table.column("name",width=220)
view_st_table.column("marks",width=30)
view_st_table.pack(fill=BOTH,expand=1)
view_st_btnback.pack(pady = 10)
view_st.withdraw()

upd_st = Toplevel(root)
upd_st.title("UPDATE STUDENT")
upd_st.geometry("400x400+400+100")

upd_st_lblrno = Label(upd_st, text='ENTER RNO', font=('courier',18,'bold'))
upd_st_entrno = Entry(upd_st, bd = 5, font=('courier',18,'bold'))
upd_st_lblname = Label(upd_st, text='ENTER NAME', font=('courier',18,'bold'))
upd_st_entname = Entry(upd_st, bd = 5, font=('courier',18,'bold'))
upd_st_lblmarks = Label(upd_st, text='ENTER MARKS(0-100)',font=('courier',18,'bold'))
upd_st_entmarks = Entry(upd_st, bd = 5, font=('courier',18,'bold'))
upd_st_btnsave = Button(upd_st, text='SAVE', font=('courier',18,'bold'),command=f10)
upd_st_btnback = Button(upd_st, text='BACK', font=('courier',18,'bold'),command=f6)

upd_st_lblrno.pack(pady = 6)
upd_st_entrno.pack(pady = 6)
upd_st_lblname.pack(pady = 6)
upd_st_entname.pack(pady = 6)
upd_st_lblmarks.pack(pady = 6)
upd_st_entmarks.pack(pady = 6)
upd_st_btnsave.pack(pady = 6)
upd_st_btnback.pack(pady = 6)
upd_st.withdraw()

del_st = Toplevel(root)
del_st.title("DELETE STUDENT")
del_st.geometry("400x400+400+100")

del_st_lblrno = Label(del_st, text='ENTER RNO', font=('courier',18,'bold'))
del_st_entrno = Entry(del_st, bd = 5 , font=('courier',18,'bold'))
del_st_btnsave = Button(del_st, text='SAVE', font=('courier',18,'bold'),command=f11)
del_st_btnback = Button(del_st, text='BACK',font=('courier',18,'bold'),command=f8)

del_st_lblrno.pack(pady = 10)
del_st_entrno.pack(pady = 10)
del_st_btnsave.pack(pady = 10)
del_st_btnback.pack(pady = 10)
del_st.withdraw()

root.mainloop()