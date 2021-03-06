import tkinter as tk

from tkinter import *
from tkinter import filedialog

# TODO: Create logs folder if it not exists

class AnalyzerApp(tk.Tk):
    
    def __init__(self, analyzer):
        super().__init__()

        self.open_status_name = False
        self.analyzer = analyzer

        w = 1100 # width for the Tk self
        h = 700 # height for the Tk self

        # Get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # Calculate x and y coordinates for the Tk self window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.title('CAnalyzer')
        self.resizable(0,0)
        self.configure(bg='#949494')

        self.geometry(f'{w}x{h}+{int(x)}+{int(y - 50)}')

        # Bind global shortcuts
        self.bind_all('<Control-n>', self.new_file)
        self.bind_all('<Control-o>', self.open_file)
        self.bind_all('<Control-s>', self.save_file)
        self.bind_all('<Control-Shift-s>', self.save_as_file)
        self.bind_all('<Control-Shift-o>', self.save_analyzed_code_as)
        self.bind_all('<F5>', self.run)

        # Create main frame
        self.main_frame = Frame(self)
        self.main_frame.pack(side=TOP, padx=2, pady=2)

        # Subsidiary frames
        self.text_input_frame = Frame(self.main_frame)
        self.text_input_frame.pack(side=LEFT)

        self.output_frame = Frame(self.main_frame)
        self.output_frame.pack(side=RIGHT)

        # Error output frame
        self.error_frame = Frame(self)
        self.error_frame.pack(side=BOTTOM, padx=2, pady=2)

        # Create scrollbars
        self.text_scroll = Scrollbar(self.text_input_frame)
        self.text_scroll.pack(side=RIGHT, fill=Y)

        self.output_scroll = Scrollbar(self.output_frame)
        self.output_scroll.pack(side=RIGHT, fill=Y)

        self.error_scroll = Scrollbar(self.error_frame)
        self.error_scroll.pack(side=RIGHT, fill=Y)

        # Create text box
        self.text_box = Text(self.text_input_frame, 
                            width=87, 
                            height=35,
                            font=('Courier', 10),
                            undo=True, 
                            yscrollcommand=self.text_scroll.set)

        self.text_box.pack()
        self.text_scroll.config(command=self.text_box.yview)

        # Create output
        self.output_box = Text(self.output_frame, 
                            width=45, 
                            height=35,
                            font=('Courier', 10),
                            state=DISABLED,
                            yscrollcommand=self.output_scroll.set)

        self.output_box.pack()
        self.output_scroll.config(command=self.output_box.yview)
        self.output_box.bind("<1>", lambda event: self.output_box.focus_set())

        # Create error output
        self.error_box = Text(self.error_frame, 
                            width=140, 
                            height=10,
                            font=('Courier', 10),
                            state=DISABLED,
                            yscrollcommand=self.error_scroll.set)

        self.error_box.pack()
        self.error_scroll.config(command=self.error_box.yview)
        self.error_box.bind("<1>", lambda event: self.error_box.focus_set())

        # Create menu
        self.top_bar = Menu(self)
        self.config(menu=self.top_bar)

        # TODO: Read label values from a file
        # Add file menu
        self.file_menu = Menu(self.top_bar, tearoff=False)
        self.top_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='New                                                        Ctrl+N', command=self.new_file)
        self.file_menu.add_command(label='Open                                                      Ctrl+O', command=self.open_file)
        self.file_menu.add_command(label='Save                                                        Ctrl+S', command=self.save_file)
        self.file_menu.add_command(label='Save As                                        Ctrl+Shift+S', command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save Analyzed Code As            Ctrl+Shift+O', command=self.save_analyzed_code_as)

        # Add run menu
        self.run_menu = Menu(self.top_bar, tearoff=False)
        self.top_bar.add_cascade(label='Run', menu=self.run_menu)
        self.run_menu.add_command(label='Run            F5', command=self.run)


    # New file function
    def new_file(self, event=None):
        self.text_box.delete('1.0', END)

        self.output_box.configure(state=NORMAL)
        self.output_box.delete('1.0', END)
        self.output_box.configure(state=DISABLED)

        self.error_box.configure(state=NORMAL)
        self.error_box.delete('1.0', END)
        self.error_box.configure(state=DISABLED)

        self.title('New File - CAnalyzer')

        self.open_status_name = False

    # Open file function
    def open_file(self, event=None):
        text_file = filedialog.askopenfilename(title='Open File', filetypes=[('C Files', '*.c')])

        if text_file:
            self.text_box.delete('1.0', END)
            
            self.output_box.configure(state=NORMAL)
            self.output_box.delete('1.0', END)
            self.output_box.configure(state=DISABLED)

            self.error_box.configure(state=NORMAL)
            self.error_box.delete('1.0', END)
            self.error_box.configure(state=DISABLED)

            # Save the status
            self.open_status_name = text_file

            file_name = text_file.split('/')[-1]

            self.title(f'{file_name} - CAnalyzer')

            # Read file contents and show them
            file_contents = ''
            with open(text_file, 'r') as f:
                file_contents = f.read()
        
            self.text_box.insert(END, file_contents)


    # Save As file function
    def save_as_file(self, event=None):
        text_file = filedialog.asksaveasfilename(title='Save As', defaultextension='.*', filetypes=[('C Files', '*.c')])
        if text_file:
            self.open_status_name = text_file

            file_name = text_file.split('/')[-1]

            self.title(f'{file_name} - CAnalyzer')

            # Write text box contents to file
            with open(text_file, 'w') as f:
                f.write(self.text_box.get(1.0, END))


    # Save file function
    def save_file(self, event=None):
        if self.open_status_name:
            # Write text box contents to file
            with open(self.open_status_name, 'w') as f:
                f.write(self.text_box.get(1.0, END))
        else:
            self.save_as_file()
    

    # Run translator
    def run(self, event=None):
        code = self.text_box.get(1.0, END)

        if code != '\n':
            analyzed_code, errors = self.analyzer.analyze_code(code)

            self.output_box.configure(state=NORMAL)
            self.output_box.delete('1.0', END)
            self.output_box.insert(END, analyzed_code)
            self.output_box.configure(state=DISABLED)

            self.error_box.configure(state=NORMAL)
            self.error_box.delete('1.0', END)
            self.error_box.insert(END, errors)
            self.error_box.configure(state=DISABLED)
    

    def save_analyzed_code_as(self, event=None):
        analyzed_code = self.output_box.get(1.0, END)
        errors = self.error_box.get(1.0, END)

        # Get the data to save
        export_txt = ''
        if analyzed_code != '\n':
            export_txt += f'Analyzed code:\n{analyzed_code}\n'

        if errors != '\n':
            export_txt += f'Errors:\n{errors}'

        if export_txt != '':
            text_file = filedialog.asksaveasfilename(title='Save As', defaultextension='.json', filetypes=[('Text', '*.txt'), ('JSON', '*.json')])
            if text_file:

                # What kind of file
                if text_file.split('.')[1] == 'txt':
                    # Write data to file
                    with open(text_file, 'w') as f:
                        f.write(export_txt)
                else:
                     # Write data to file
                    with open(text_file, 'w') as f:
                        f.write(self.analyzer.serialize_output_and_errors())
