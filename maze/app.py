
import tkinter as tk
from tkinter import ttk, messagebox
from .game import Maze
from . import ai as ai_impl
from common import plugins, profiling

CELL=20
def main():
    root=tk.Tk(); root.title("HW1 Maze — BFS/DFS/Dijkstra/A*/GBFS")
    m=Maze(); m.generate_random(); path=[]
    frm=ttk.Frame(root,padding=8); frm.pack()
    canvas=tk.Canvas(frm,width=m.cols*CELL,height=m.rows*CELL,bg="white"); canvas.grid(row=0,column=0,columnspan=5,padx=6,pady=6)
    alg=tk.StringVar(value="RANDOM")
    for i,(lbl,val) in enumerate([("Random","RANDOM"),("BFS","BFS"),("DFS","DFS"),("Dijkstra","DIJKSTRA"),("A*","ASTAR"),("GBFS","GBFS")]):
        ttk.Radiobutton(frm,text=lbl,variable=alg,value=val).grid(row=1,column=i,sticky="w")
    ttk.Label(frm,text="Heuristic:").grid(row=2,column=0,sticky="e")
    names=plugins.list_names("maze") or ["zero"]
    hvar=tk.StringVar(value=names[0])
    ttk.Combobox(frm,textvariable=hvar,values=names,state="readonly",width=12).grid(row=2,column=1,sticky="w")
    tvar=tk.StringVar(value="Last solve: n/a"); ttk.Label(frm,textvariable=tvar).grid(row=3,column=0,columnspan=5,sticky="w")
    def draw():
        canvas.delete("all")
        for r in range(m.rows):
            for c in range(m.cols):
                x0,y0=c*CELL,r*CELL; x1,y1=x0+CELL,y0+CELL
                if m.grid[r][c]==0:  # Unwalkable (black)
                    canvas.create_rectangle(x0,y0,x1,y1,fill="black")
                elif m.grid[r][c]==5:  # Weight 5 (blue)
                    canvas.create_rectangle(x0,y0,x1,y1,fill="lightblue")
                # Weight 1 (white) - default background, no fill needed
        sr,sc=m.start; gr,gc=m.goal
        canvas.create_rectangle(sc*CELL,sr*CELL,sc*CELL+CELL,sr*CELL+CELL,fill="green")
        canvas.create_rectangle(gc*CELL,gr*CELL,gc*CELL+CELL,gr*CELL+CELL,fill="red")
        for (r,c) in path: canvas.create_rectangle(c*CELL+4,r*CELL+4,c*CELL+CELL-4,r*CELL+CELL-4,outline="blue")
    def solve():
        nonlocal path
        metrics={}
        try:
            with profiling.timer() as t:
                if alg.get()=="BFS":
                    path, expanded =ai_impl.bfs(m)
                elif alg.get()=="DFS":
                    path, expanded =ai_impl.dfs(m)
                elif alg.get()=="DIJKSTRA":
                    path, expanded =ai_impl.dijkstra(m)
                elif alg.get()=="ASTAR":
                    h=plugins.get("maze", hvar.get()); path, expanded=ai_impl.a_star(m, h)
                elif alg.get()=="GBFS":
                    h=plugins.get("maze", hvar.get()); path, expanded =ai_impl.gbfs(m, h)
            tvar.set(f"Last solve: {t['seconds']*1000:.1f} ms; nodes expanded={len(expanded)}; path length={len(path)}")
        except NotImplementedError:
            messagebox.showinfo("AI not implemented","Implement BFS/DFS/Dijkstra/A*/GBFS in maze/ai.py"); path=[]
        draw()
    ttk.Button(frm,text="Solve",command=solve).grid(row=2,column=2,padx=6)
    ttk.Button(frm,text="Regenerate",command=lambda:(m.generate_random(),draw())).grid(row=2,column=3,padx=6)
    draw(); root.mainloop()
if __name__=="__main__": main()
