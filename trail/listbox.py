import tkinter as tk

window = tk.Tk()
window.geometry('1000x500')

lbx_info = ['short frase', 'medium sentence', 'the longest sentence in the list']
lbl_bg = ['#ff0000', '#ffff00', '#00cc00']

lbx = tk.Listbox(window, font='Arial 20', bd=10)
for e in lbx_info:
    lbx.insert(tk.END, e)
lbx.place(x=0, y=0)


name_lbl = tk.Label(window, font='Arial 16')
name_lbl.place(x=500, y=0)
def show(pos):
    name_lbl.configure(text=f'Nome: {lbx_info[pos[0]]}', bg=f'{lbl_bg[pos[0]]}')


lbx.bind('<<ListboxSelect>>', lambda m: show(lbx.curselection()))
window.mainloop()
