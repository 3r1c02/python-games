import tkinter as tk
import time
from tkinter import messagebox


class Frame:
    """Stellt ein Raster von Zellen dar, deren Farbe geändert werden kann"""

    def __init__(self, title="Frame", width=800, height=800, count_x=10, count_y=10, has_border=False):
        self.canvas_size_x = width
        self.canvas_size_y = height
        unit_x = width / count_x
        unit_y = height / count_y
        self.cell_size = unit_x
        self.cell_count = count_x * count_y
        self.cell_count_x = count_x
        self.cell_count_y = count_y

        self.time = -1
        self.__event_queue = []

        self.window = tk.Tk()
        self.window.title(title)
        self.canvas = tk.Canvas(self.window, width=width, height=height)
        self.canvas.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.__on_quit)
        self.running = True
        self.window.bind("<Key>", self.__on_key)
        self.window.bind("<Motion>", self.__on_motion)
        self.window.bind("<Button-1>", self.__on_click)

        self.rects = []
        self.__colors = ["white"] * count_x * count_y
        for row in range(count_y):
            for col in range(count_x):
                x = col * unit_x
                y = row * unit_y
                rect = self.canvas.create_rectangle(
                    x, y, x + unit_x, y + unit_y,
                    fill="white",
                    width=1 if has_border else 0
                )
                self.rects.append(rect)

    def set_color(self, x, y, color):
        """Ändert die Farbe einer Zelle
        
        `x` und `y` sind die Koordinaten der Zelle (von oben links nach unten rechts)
        
        `color` ist entweder:
         * ein englischer Farbname als string (z.B. `"white"` oder `"red"`)
         * ein Farbcode in hexadezimaler Schreibweise als string (z.B. `"#FF0000"` für rot)
         * ein Farbcode, der mir der Funktion `color_from_rgb(...)` berechnet werden kann
        """

        self.__validate_cell(x, y)
        index = int(y) * self.cell_count_x + int(x)
        self.__colors[index] = color
        rect = self.rects[index]
        self.canvas.itemconfig(rect, fill=color)

    def clear(self, color="white"):
        """Setzt alle Zellen auf dieselbe Farbe
        
        Für color gilt das gleiche wie bei `set_color`.

        Wird keine Farbe angegeben, wird weiß verwendet.
        """
        for x in range(self.cell_count_x):
            for y in range(self.cell_count_y):
                self.set_color(x, y, color)

    def get_color(self, x, y):
        """Gibt die aktuelle Farbe einer Zelle zurück"""
        self.__validate_cell(x, y)
        index = int(y) * self.cell_count_y + int(x)
        return self.__colors[index]

    def close(self):
        """Schließt das Fenster"""
        self.running = False
        self.window.destroy()

    def get_events(self, tick_interval=0.016):
        """Hält das Fenster offen und gibt die auftretenden Ereignisse zurück

        Über `tick_interval` kann optional eingestellt werden,
        in welchen Zeitabständen das `tick`-Ereignis auftreten soll.
        
        Sollte in einer for-Schleife verwendet werden:
        ```python
            for event in frame.get_events():
                # irgendwas damit machen
        ```
        """
        self.time = time.time()
        while self.running:
            self.window.update()

            now = time.time()
            if now - self.time >= tick_interval:
                yield TickEvent(now)
                self.time = now

            while len(self.__event_queue) > 0:
                yield self.__event_queue.pop(0)

    def __validate_cell(self, x, y):
        if x >= 0 and x < self.cell_count_x and y >= 0 and y < self.cell_count_y:
            return

        messages = []
        if x < 0:
            messages.append(f"x ist zu klein ({x} < 0)")
        elif x >= self.cell_count_x:
            messages.append(f"x ist zu groß ({x} > {self.cell_count_x})")
        if y < 0:
            messages.append(f"y ist zu klein ({y} < 0)")
        elif y >= self.cell_count_y:
            messages.append(f"y ist zu groß ({y} > {self.cell_count_y})")
        raise IndexError(", ".join(messages))

    def __on_quit(self):
        self.running = False

    def __on_key(self, event):
        self.__event_queue.append(KeyEvent(event.keysym))

    def __on_motion(self, event):
        self.__event_queue.append(MouseMoveEvent(self.__cell_from_coords(event.x, event.y)))

    def __on_click(self, event):
        self.__event_queue.append(ClickEvent(self.__cell_from_coords(event.x, event.y)))

    def __cell_from_coords(self, x, y):
        return (
            int(max(0, min(self.cell_count_x - 1, x // self.cell_size))),
            int(max(0, min(self.cell_count_y - 1, y // self.cell_size)))
        )


class TickEvent:
    """Ein Ereignis, das in regelmäßigen Abständen auftritt
    
    Eigenschaften:
     * `type`: immer `"tick"`, zum Identifizieren
     * `time`: die aktuelle Zeit in Sekunden
    """

    def __init__(self, time):
        self.type = "tick"
        self.time = time

    def get_time_ms(self):
        return int(self.time * 1000)


class KeyEvent:
    """Ein Ereignis, das auftritt wenn eine Taste gedrückt wird
    
    Eigenschaften:
     * `type`: immer `"key"`, zum Identifizieren
     * `key`: Der Name der Taste
    """

    def __init__(self, key):
        self.type = "key"
        self.key = key


class MouseMoveEvent:
    """Ein Ereignis, das auftritt wenn die Maus bewegt wird
    
    Eigenschaften:
     * `type`: immer `"mouse_move"`, zum Identifizieren
     * `x`, `y`: Die Koordinaten der Zelle, über der sich die Maus befindet
     * `cell`: Die Koordinaten der Zelle als Tupel
    """

    def __init__(self, cell):
        self.type = "mouse_move"
        self.cell = cell
        self.x, self.y = cell


class ClickEvent:
    """Ein Ereignis, das auftritt wenn auf eine Zelle geklickt wird
    
    Eigenschaften:
     * `type`: immer `"click"`, zum Identifizieren
     * `x`, `y`: Die Koordinaten der Zelle, über der sich die Maus befindet
     * `cell`: Die Koordinaten der Zelle als Tupel
    """

    def __init__(self, cell):
        self.type = "click"
        self.cell = cell
        self.x, self.y = cell


def color_from_rgb(r, g, b):
    """Konvertiert eine Farbe aus RGB-Werten in ihren Hexadezimalcode"""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


class Return:
    """Ausgabe von Informationen an den User"""

    def messagebox(name, info):
        """
        Zeige ein Information in einem Fenster an.
        :param name: Titel des Fensters
        :param info: Inhalt des Fensters
        :return:
        """
        messagebox.showinfo(name, info)


class Input:
    """Abfrage von Informationen"""

    def asklist(self, option1, option2, option3):
        list = tk.Tk()

        def output():
            currently_selected = Lb.curselection()
            list.destroy()
            global asklist_var
            asklist_var = currently_selected

        Lb = tk.Listbox(list)
        Lb.insert(1, option1)
        Lb.insert(2, option2)
        Lb.insert(3, option3)
        Lb.pack()
        confirm = tk.Button(list, text="Confirm", command=output)
        confirm.pack()
        list.mainloop()
        return asklist_var