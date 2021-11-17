import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

root = tk.Tk()

root.geometry("1000x1000") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.

root.configure(bg='#FFEBB0')

dataframe = pd.read_csv('Table_points.csv')

names=dataframe['Name'].tolist()
intvar=[]

frame1 = tk.LabelFrame(root, text="Points Table",bg='gold2')
frame1.place(height=250, width=1000)

frame2=tk.LabelFrame(root)
frame2.place(rely=0.7,height=250,width=1000)

## Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)

tv1["column"] = list(dataframe.columns)
tv1["show"] = "headings"
for column in tv1["columns"]:
    tv1.heading(column, text=column) # let the column heading = column name

    df_rows = dataframe.to_numpy().tolist() # turns the dataframe into a list of lists
for row in df_rows:
    tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert


for i in range(len(names)):
    # Append int variables for each checkbox
    option = tk.IntVar()
    option.set(0)
    intvar.append(option)
tk.Label(root,text='Tick two players').place(rely=0.45)  
for i in range(len(names)):
    tk.Checkbutton(root,text=names[i],variable=intvar[i],bg='gold2').place(relx=0.1*i,rely=0.5)

tk.Label(root,text='Enter name of the winner').place(rely=0.55)
entry=tk.Entry(root)
entry.place(rely=0.6)

tk.Button(root, text="OK",
command=lambda: getInfo(entry.get())).place(rely=0.63)

tk.Button(root,text='update Table',command=lambda: update()).place(rely=0.66)

def getInfo(winner):
    players=[]
    for i in range(len(names)):
        #Get services variable
        if intvar[i].get()==1:
            players.append(i)
    if len(players)!=2:
        raise tk.messagebox.showerror(title='error',message="Please Choose two players") 
        
    
    if winner not in names:
        raise tk.messagebox.showerror(title='error',message='Enter a valid name')
    
    index1=players[0]
    index2=players[1]
    
    
    player1=names[index1]
    player2=names[index2]
    
    update_rank(player1,player2,winner,dataframe)
    

def update_rank(player1,player2,winner,df):
    a=df.loc[df['Name']==player1].values.tolist()
    b=df.loc[df['Name']==player2].values.tolist()

    drop_index1=df.loc[df['Name']==player1].index.values[0]
    drop_index2=df.loc[df['Name']==player2].index.values[0]

    df=df.drop(index=drop_index1,axis=0)
    df=df.drop(index=drop_index2,axis=0)
    
    details1=[]
    details2=[]

    for x in a[0]:
        details1.append(x)
    for x in b[0]:
        details2.append(x)
    Player1=Player(details1[0],details1[1],details1[2])
    Player2=Player(details2[0],details2[1],details2[2])
    if Player1.name==winner:
        if Player1.rank+1==Player2.rank or Player2.rank+1==Player2:
            if Player1.rank<Player2.rank:
      #Player1.case0()
              Player2.case5()
            else:
              Player1.case2()
              Player2.case5()
        if Player1.rank+2==Player2.rank or Player2.rank+2==Player2:
            if Player1.rank<Player2.rank:
                Player1.case1()
                Player2.case6()
            else:
                Player1.case3()
                Player2.case6()
    if Player2.name==winner:
        if Player1.rank+1==Player2.rank or Player2.rank+1==Player2:
            if Player1.rank<Player2.rank:
                Player1.case5()
                Player2.case2()
            else:
                Player1.case4()
  
        if Player1.rank+2==Player2.rank or Player2.rank+2==Player1.rank:
            if Player1.rank<Player2.rank:
                Player2.case3()
                Player1.case6()
            else:
                Player2.case1()
                Player1.case6()
                
                
    l,m=Player1.update(),Player2.update()
    l=[l]
    m=[m]

    df = df.append(pd.DataFrame( l,columns=[ 'Name', 'Points', 'Rank']),ignore_index = True)
    df = df.append(pd.DataFrame( m,columns=[ 'Name', 'Points', 'Rank']),ignore_index = True)

    df.sort_values('Points', axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last', ignore_index=True, key=None)
    df['Rank']=df['Points'].rank(ascending=False,method='first')
    df.to_csv('Table_points.csv',index=False)
        
    
def update():
## Treeview Widget
    df2=pd.read_csv('Table_points.csv')
    tv2 = ttk.Treeview(frame2)
    tv2.place(relheight=1, relwidth=1)

    tv2["column"] = list(df2.columns)
    tv2["show"] = "headings"
    for column in tv2["columns"]:
        tv2.heading(column, text=column) # let the column heading = column name

        df_rows = df2.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv2.insert("", "end", values=row) #    

class Player:
  def __init__(self,name,points,rank):
    self.name=name
    self.points=points
    self.rank=rank
  def case0(self):
    self.points+=0
  def case1(self):
    self.points+=1
  def case2(self):
    self.points+=2
  def case3(self):
    self.points+=3
  def case4(self):
    self.points-=1
  def case5(self):
    self.points-=2
  def case6(self):
    self.points-=3
  
  def update(self):
    return [self.name,self.points,self.rank]

root.mainloop()