from tkinter import *
from tkinter import ttk
from pytube import YouTube
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
import io
import os

class Youtube_app:
    def __init__(self,root):
        self.root = root
        self.root.title("Youtube Downloader ")
        self.root.geometry("800x600+300+50")
        self.root.resizable(False,False)
        

        self.AppBar = Frame(self.root, width=400, height=30,bg='black', bd=9, relief="raise")
        self.AppBar.pack(side=TOP, fill=X)

        self.bordy = Frame(self.root, width=500, height=500)
        self.bordy.pack(fill=BOTH, expand=True)
        

        lb_title = Label(self.AppBar, text='Youtube Downloader',fg='white', bg='black', font="Times 20 bold ")
        lb_title.pack(anchor=CENTER)

        
        lb_url = Label(self.bordy,text='Video URL:',fg='black' , font="Times 16 bold ",)
        lb_url.place(relx=0.0, rely=0.05)


        
        self.var_url = StringVar()
        entry_url = Entry(self.bordy,bd = 5, bg="lightyellow",textvariable=self.var_url)
        entry_url.place(relx=0.15, rely=0.05,relwidth= 0.60)


        lb_file_type = Label(self.bordy,text='File Type:',fg='black', font="Times 16 bold ")
        lb_file_type.place(relx=0.0, rely=0.15)

        #variaveis de controle do btn_video_radio
        self.var_fileType = StringVar()
        self.var_fileType.set('video')

        btn_video_radio = Radiobutton(self.bordy,text='Video',fg='black', variable= self.var_fileType, value="video", font="Times 16 bold ")
        btn_video_radio.place(relx=0.15, rely=0.15)

        btn_audio_radio = Radiobutton(self.bordy,text='Audio',fg='black' ,variable= self.var_fileType, value="audio", font="Times 16 bold ")
        btn_audio_radio.place(relx=0.30, rely=0.15)

        btn_audio_radio = Radiobutton(self.bordy,text='Audio',fg='black' ,variable= self.var_fileType, value="audio", font="Times 16 bold ")
        btn_audio_radio.place(relx=0.45, rely=0.15)

        btn_search=Button(self.bordy,  text='search', width=15, bg='red', fg="#fff", relief='flat', highlightbackground='#524f4f',command=self.search)
        btn_search.place(relx=0.80, rely=0.05)

        frame_info = Frame(self.bordy, bd=2,relief="raise", bg ='lightyellow')
        frame_info.place(relx=0.002, rely=0.20, relwidth=0.99 ,relheight=0.5 )  

        self.lb_video_title =  Label(frame_info, text='Video title Here', font="Times 12 ",bg='light slate gray' ,fg='white', anchor='w')
        self.lb_video_title.place(relx=0.0, rely=0.0, relwidth=1)

        self.lb_video_image =  Label(frame_info ,text='Video \n image', font="Times 12 ",bg='light slate gray' ,fg='white',bd =2, relief="raise")
        self.lb_video_image.place(relx=0.01,rely=0.15, relwidth=0.40 ,relheight=0.80)

        lb_description = Label(frame_info ,text='description:', bg='lightyellow' , font="Times 16 bold ")
        lb_description.place(relx=0.42,rely=0.12)

        self.textfield_description = Text(frame_info , bg='lightyellow' , font="Times 16 bold ")
        self.textfield_description.place(relx=0.42,rely=0.30, relwidth=0.56 ,relheight=0.60)


        self.lb_size = Label(self.bordy,text='Total Size: 0 MB',fg='black' , font="Times 16 bold ")
        self.lb_size.place(relx=0.0, rely=0.72)


        btn_clear=Button(self.bordy,  text='Clear', bg='gray', fg="#fff", relief='flat', highlightbackground='#524f4f',command=self.clear)
        btn_clear.place(relx=0.01, rely=0.77)


        self.btn_download=Button(self.bordy,  text='Download', state= DISABLED, bg='green', fg="#fff", relief='flat', highlightbackground='#524f4f',command=self.download)
        self.btn_download.place(relx=0.1, rely=0.77)

        self.prog_bar = ttk.Progressbar(self.root, orient = HORIZONTAL, length=590, mode='determinate')
        self.prog_bar.place(relx=0.01, rely=0.85, relwidth=0.98, relheight=0.05 )
        
        self.lb_download = Label(self.bordy,text='Downloading: 0% ',fg='black' , font="Times 16 bold ")
        self.lb_download.place(relx=0.011, rely=0.90)

        if os.path.exists('audios') == False:
            os.mkdir('audios')
        if os.path.exists('videos')== False:
            os.mkdir('videos')

    def search(self):
        if self.var_url.get()=="":
            messagebox.showinfo("INFO","Video URL is required")  
        else:
           
            yt = YouTube(self.var_url.get())
            
            
            
            # connverte thumbnail em imagem
            response = requests.get(yt.thumbnail_url)
            img_byte=io.BytesIO(response.content)
            self.img = Image.open(img_byte)
            self.img = self.img.resize((300,200),Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
          
            # exibir a imagem no modal
            self.lb_video_image.config(image=self.img)
            
            # Verificando o tipo
            if self.var_fileType.get() == "audio":
                select_file = yt.streams.filter(only_audio=True).first()
            
            if self.var_fileType.get() == "video":
                select_file = yt.streams.filter(progressive=True).first()
            
            self.size_inBytes = select_file.filesize
            max_size =  self.size_inBytes / 1024000
            self.mb = round(max_size,2)

         

            # deploy na interface dos valores da aplicação"
            self.lb_size.config(text="Total Size: {} MB".format(self.mb))
            self.lb_video_title.config(text=yt.title)
            self.textfield_description.delete('1.0',END)
            self.textfield_description.insert(END,yt.description[:200])
            self.btn_download.config(state=NORMAL)

    def progress_(self,streams,chunk,bytes_remaining):

        percentage = (float(abs(bytes_remaining-self.size_inBytes)/self.size_inBytes))*float(100)
        self.prog_bar['value'] = percentage
        self.prog_bar.update()
        self.lb_download.config(text="Downloading: {}%".format(str(round(percentage,2))))

        if round(percentage,2) == 100:
            messagebox.showinfo("INFO","Download Completed")   
            self.btn_download.config(state=DISABLED)

    def download(self):

        yt = YouTube(self.var_url.get(),on_progress_callback=self.progress_)

        if self.var_fileType.get() == "audio":
            select_file = yt.streams.filter(only_audio=True).first()
            select_file.download('audios/')
        
        if self.var_fileType.get() == "video":
            select_file = yt.streams.filter(progressive=True).first()
            select_file.download('videos/')

    def clear(self):
        self.var_fileType.set('video')
        self.var_url.set('')
        self.prog_bar['value']=0
        self.btn_download.config(state=DISABLED)
        self.lb_video_title.config(text="Video title Here")
        self.lb_video_image.config(image='')
        self.textfield_description.delete('1.0',END)
        self.lb_size.config(text="Total Size: 0 MB")
        self.lb_download.config(text='Downloading: 0% ')

root = Tk()
obj_instace = Youtube_app(root)
root.mainloop()

