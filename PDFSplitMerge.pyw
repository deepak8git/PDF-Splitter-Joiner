from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import os
import subprocess
import img2pdf
from PIL import Image
import sys



iMaxStackSize = 5000
sys.setrecursionlimit(iMaxStackSize)

def browse_split_source_button():
    global split_folder_path
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    split_folder_path.set(filename)
    #print(split_folder_path.get())
    #print(os.path.dirname(folder_path.get()))

def browse_split_destination_button():
    global split_des_folder_path
    filename=filedialog.askdirectory()
    split_des_folder_path.set(filename)
    #print(split_des_folder_path.get())
    
def splitToPDF():
    #try:
        #print(split_des_folder_path.get())
        inputpdf = PdfFileReader(open(split_folder_path.get(), "rb"),strict=False)
        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open(split_des_folder_path.get() + "/pdfpage%02d.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
    
        messagebox.showinfo("Info","PDF File Splitted Successfully")
        subprocess.run(['explorer', os.path.realpath(split_des_folder_path.get())])
    #except:
    #   messagebox.showerror("Warning","Some Error Occured")
    #finally:
    #    split_folder_path.set("")
    #    split_des_folder_path.set("")


def browse_merge_source_button():
    global merge_folder_path
    filename = filedialog.askdirectory()  # askdirectory()
    merge_folder_path.set(filename)

def browse_merge_destination_button():
    global merge_des_folder_path
    filename=filedialog.asksaveasfilename(initialdir = "/",title = "Save file",defaultextension="*.pdf",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    merge_des_folder_path.set(filename)
    #messagebox.showinfo("file name", merge_des_folder_path.get())


def mergeToPDF():
    try:
        x = [os.path.abspath(os.path.join(merge_folder_path.get(), a)) for a in os.listdir(merge_folder_path.get()) if a.endswith(".pdf")]
        merger = PdfFileMerger()

        for pdf in x:
            fread = open(pdf, 'rb')
            merger.append(fread)

        with open(merge_des_folder_path.get(), "wb") as fout:
            merger.write(fout)
            fout.close()
            fread.close()

        messagebox.showinfo("Info","PDF File Merged Successfully")
        subprocess.run(['explorer', os.path.realpath(merge_des_folder_path.get())])

    except:
        messagebox.showerror("Warning","Some Error Occured")
    finally:    
        merge_folder_path.set("")
        merge_des_folder_path.set("")


def browse_img2pdf_source_button():
    global img2pdf_folder_path
    if(rvalue.get()==1):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = \
                                        (("jpg files","*.jpg"),("all files","*.*")))
    else:
        filename = filedialog.askdirectory()  # askdirectory()
    img2pdf_folder_path.set(filename)



def browse_img2pdf_destination_button():
    global img2pdf_dest_folder_path
    if(rvalue.get() == 2):
        filename = filedialog.askdirectory()  # askdirectory()
    elif(rvalue.get() == 3 or rvalue.get() == 1):
        filename = filedialog.asksaveasfilename(initialdir = "/",title = "Save file",defaultextension="*.pdf",filetypes = \
                    (("pdf files","*.pdf"),("all files","*.*")))
    img2pdf_dest_folder_path.set(filename)


def imageToPDF():
    if(rvalue.get() == 1):
        imageToPDFSingle()
    elif(rvalue.get() == 2):
        imageToPDFSeparate()
    elif(rvalue.get()==3):
        imageToPDFAllMerge()
    else:
        messagebox.showerror("Warning","Kindly Select the Proper Options")   

    img2pdf_folder_path.set("") 
    img2pdf_dest_folder_path.set("") 

def imageToPDFSingle():
    img_path = img2pdf_folder_path.get()
    new_path=img2pdf_dest_folder_path.get()
    #print(new_path)
    image = Image.open(img_path)
    pdf_path=new_path.rsplit('.', 1)[0] + '.pdf'
    pdf_bytes=img2pdf.convert(image.filename)
    with open(pdf_path,"wb") as file:
        file.write(pdf_bytes)
    image.close()
    messagebox.showinfo("info","Successfully Converted Image File to PDF File") 
    subprocess.run(['explorer', os.path.realpath(img2pdf_dest_folder_path.get())])


def imageToPDFSeparate():
    x = [os.path.abspath(os.path.join(img2pdf_folder_path.get(), a)) for a in os.listdir(img2pdf_folder_path.get()) if a.endswith(".jpg")]

    for img_path in x:
        new_path=os.path.abspath(os.path.join(img2pdf_dest_folder_path.get(), os.path.basename(img_path)))
        image = Image.open(img_path)
        
        pdf_path=new_path.rsplit('.', 1)[0] + '.pdf'
        pdf_bytes=img2pdf.convert(image.filename)
        with open(pdf_path,"wb") as file:
            file.write(pdf_bytes)
        image.close()
    messagebox.showinfo("info","Successfully Converted Image File to PDF File") 
    subprocess.run(['explorer', os.path.realpath(img2pdf_dest_folder_path.get())])


def imageToPDFAllMerge():
    filelist=[]
    x = [os.path.abspath(os.path.join(img2pdf_folder_path.get(), a)) for a in os.listdir(img2pdf_folder_path.get()) if a.endswith(".jpg")]
    merger = PdfFileMerger()
    
    for img_path in x:
            #new_path=os.path.abspath(os.path.join(img2pdf_dest_folder_path.get(), os.path.basename(img_path)))
        pdf_path=img_path.rsplit('.', 1)[0] + '.pdf'

        with Image.open(img_path) as img:
            pdf_bytes=img2pdf.convert(img.filename)
            filelist.append(pdf_path)  
               
        with open(pdf_path,"wb") as file:
            file.write(pdf_bytes)
            file.close()
          
        f=open(pdf_path, 'rb')
        merger.append(f)
        
        #merger.append(open(pdf_path, 'rb'))            
           
    with open(img2pdf_dest_folder_path.get(), "wb") as fout:
        merger.write(fout)
        fout.close()
        f.close()

    #for f in filelist:
    #    os.remove(f)
    messagebox.showinfo("info","Image File Converted and Merged Successfully") 
    subprocess.run(['explorer', os.path.realpath(img2pdf_dest_folder_path.get())])
    

def browse_extractPDF_source_button():
    global extractPDF_folder_path
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    extractPDF_folder_path.set(filename)

def browse_extractPDF_destination_button():
    global extractPDF_dest_folder_path
    filename=filedialog.asksaveasfilename(initialdir = "/",title = "Save file",defaultextension="*.pdf",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    #filename=filedialog.askdirectory()
    extractPDF_dest_folder_path.set(filename)
 
def extractPageFromPDF():
    try:

        #print(getPDFPageNumber(extractPDFPageNumber.get()))
        pageNumber = getPDFPageNumber(extractPDFPageNumber.get())
        output = PdfFileWriter()
        inputpdf = PdfFileReader(open(extractPDF_folder_path.get(), "rb"),strict=False)
        
        for i in range(inputpdf.numPages):
            if(i+1 in pageNumber):
                output.addPage(inputpdf.getPage(i))

        with open(extractPDF_dest_folder_path.get(),"wb") as outputStream:
            output.write(outputStream)
        
        messagebox.showinfo("Info","PDF File Extracted Successfully")
        subprocess.run(['explorer', os.path.realpath(extractPDF_dest_folder_path.get())])

        extractPDF_dest_folder_path.set("")
        extractPDF_folder_path.set("")
        extractPDFPageNumber.set("")
    except:
        messagebox.showerror("Warning","Some Error Occured")
        


def getPDFPageNumber(pageNumberString):
    try:
        inputStr = pageNumberString #extractPDFPageNumber.get()
        listinput = list(inputStr.split(","))
        listinput = [x for x in listinput if x]

        newlist=[]
        indexlist=[]
        j=0
        for i in listinput:
            if(i.__contains__("-")):
                newdata =list(i.split("-"))
                a=int(newdata[0])
                b=int(newdata[1])
                newlist.extend(list(range(a,b+1)))
                indexlist.append(j)
            j+=1
            
        listinput.extend(newlist)
        indexlist.sort(reverse=True)
    
        for index in indexlist:
            del listinput[index]
        
        listinput = list(map(int,listinput))
        listinput.sort()
        listinput=list(dict.fromkeys(listinput))

        return listinput

    except:
        messagebox.showerror("Warning","Some Error in Page Number Section")



#This section initiate Graphics and defines position and geometry of windows which opens
root =Tk()
root.title("Welcome to PDF Splitter/Merger                        Developed By: Deepak Kumar Ram")
#root.iconbitmap(r"C:\Users\Deepak\Desktop\Installer\sbi.ico")
        #root.overrideredirect(1)
root.resizable(0,0)  
root.withdraw()
root.update_idletasks()

w,h=610,200
x=(root.winfo_screenwidth() - w)/2
y=(root.winfo_screenheight() - h)/2
root.geometry("{}x{}+{}+{}".format(w,h,int(x),int(y)))
#****************************************************************************************

tabcontrol = Notebook(root)
tab1 = Frame(tabcontrol)
tabcontrol.add(tab1,text="  PDF Splitter  ")

# This section for Tab1 PDF Splitter ***************************************************
split_folder_path = StringVar()
split_des_folder_path=StringVar()

pdfSplit = LabelFrame(tab1, text=" Split Single PDF to Multiple Files ", width=585, height=100)
pdfSplit.place(x=10,y=20)
splitSourceLabel = Label(pdfSplit, text="Source")
splitSourceLabel.place(x=5, y=20, anchor="w")
splitSourceEntry = Entry(pdfSplit,width=70,textvariable=split_folder_path)
splitSourceEntry.place(x=70,y=20,anchor="w")
splitSourceButton=Button(pdfSplit,text="Browse",command=browse_split_source_button)
splitSourceButton.place(x=500,y=20,anchor="w")

splitDestinationLabel = Label(pdfSplit, text="Destination")
splitDestinationLabel.place(x=5, y=50, anchor="w")
splitDestinationEntry = Entry(pdfSplit,width=70,textvariable=split_des_folder_path)
splitDestinationEntry.place(x=70,y=50,anchor="w")
splitDestinationButton=Button(pdfSplit,text="Browse",command=browse_split_destination_button)
splitDestinationButton.place(x=500,y=50,anchor="w")

convertPDFButton = Button(tab1,text="  Split to PDF  ",command=splitToPDF)
convertPDFButton.place(x=250,y=140,anchor="w")
#****************************************************************************************

tab2 = Frame(tabcontrol)
tabcontrol.add(tab2,text="  PDF Merger  ")

# This section for Tab2 PDF Merger ***************************************************
merge_folder_path = StringVar()
merge_des_folder_path=StringVar()

pdfMerge = LabelFrame(tab2, text=" Merger Multiple PDF Files to Single File ", width=585, height=100)
pdfMerge.place(x=10,y=20)
mergeSourceLabel = Label(pdfMerge, text="Source")
mergeSourceLabel.place(x=5, y=20, anchor="w")
mergeSourceEntry = Entry(pdfMerge,width=70,textvariable=merge_folder_path)
mergeSourceEntry.place(x=70,y=20,anchor="w")
mergeSourceButton=Button(pdfMerge,text="Browse",command=browse_merge_source_button)
mergeSourceButton.place(x=500,y=20,anchor="w")

mergeDestinationLabel = Label(pdfMerge, text="Destination")
mergeDestinationLabel.place(x=5, y=50, anchor="w")
mergeDestinationEntry = Entry(pdfMerge,width=70,textvariable=merge_des_folder_path)
mergeDestinationEntry.place(x=70,y=50,anchor="w")
mergeDestinationButton=Button(pdfMerge,text="Browse",command=browse_merge_destination_button)
mergeDestinationButton.place(x=500,y=50,anchor="w")

mergePDFButton = Button(tab2,text="  Merge PDF Files  ",command=mergeToPDF)
mergePDFButton.place(x=250,y=140,anchor="w")
#****************************************************************************************

tab3 = Frame(tabcontrol)
tabcontrol.add(tab3,text="  Image to PDF  ")

#This Section is for Tab3 Image to PDF *****************************************************
rvalue=IntVar()
img2pdf_dest_folder_path=StringVar()
img2pdf_folder_path=StringVar()

imagePDFMergeConvert = LabelFrame(tab3, text=" Convert Image Files to PDF Files ", width=585, height=110)
imagePDFMergeConvert.place(x=10,y=10)

imageSingleToPDFRadio =Radiobutton(imagePDFMergeConvert, text = "Single File to PDF", variable=rvalue, value=1)
imageSingleToPDFRadio.place(x=70, y=10, anchor=W)
imageToPDFRadio = Radiobutton(imagePDFMergeConvert,text="All Image to Seperate PDF", variable=rvalue, value=2)
imageToPDFRadio.place(x=187, y=10, anchor=W)
imageToPDFMergeRadio = Radiobutton(imagePDFMergeConvert,text="All Image to PDF and Merge", variable=rvalue, value=3)
imageToPDFMergeRadio.place(x=350, y=10, anchor=W)

imageToPDFSourceLabel = Label(imagePDFMergeConvert, text="Source")
imageToPDFSourceLabel.place(x=5, y=40, anchor="w")
imageToPDFSourceEntry = Entry(imagePDFMergeConvert,width=70,textvariable=img2pdf_folder_path)
imageToPDFSourceEntry.place(x=70,y=40,anchor="w")
imageToPDFSourceButton=Button(imagePDFMergeConvert,text="Browse",command=browse_img2pdf_source_button)
imageToPDFSourceButton.place(x=500,y=40,anchor="w")

imageToPDFDestinationLabel = Label(imagePDFMergeConvert, text="Destination")
imageToPDFDestinationLabel.place(x=5, y=70, anchor="w")
imageToPDFDestinationEntry = Entry(imagePDFMergeConvert,width=70,textvariable=img2pdf_dest_folder_path)
imageToPDFDestinationEntry.place(x=70,y=70,anchor="w")
imageToPDFDestinationButton=Button(imagePDFMergeConvert,text="Browse",command=browse_img2pdf_destination_button)
imageToPDFDestinationButton.place(x=500,y=70,anchor="w")

convertImageToPDFButton = Button(tab3,text="  Convert Image to PDF Files  ",command=imageToPDF)
convertImageToPDFButton.place(x=210,y=140,anchor="w")
#****************************************************************************************

tab4 = Frame(tabcontrol)
tabcontrol.add(tab4,text="  Extract PDF Page  ")

#This Section is for Tab4 For Extracting PDF Files Based on Page Number *****************************************************
extractPDF_dest_folder_path=StringVar()
extractPDF_folder_path=StringVar()
extractPDFPageNumber =StringVar()


extractPDFConvert = LabelFrame(tab4, text=" Extract Page from PDF File ", width=585, height=110)
extractPDFConvert.place(x=10,y=10)

extractPDFPageNoLabel = Label(extractPDFConvert, text="Page Range")
extractPDFPageNoLabel.place(x=5, y=10, anchor="w")
extractPDFPageNoEntry = Entry(extractPDFConvert,width=15,textvariable=extractPDFPageNumber)
extractPDFPageNoEntry.place(x=75,y=10,anchor="w")
extractPDFPageNoDetailsLabel = Label(extractPDFConvert, text="Hint:For Single Page Enter 3 or 4 or 1,3 or 4,5,7 For Range 4-8 or 2,4,6-9,11-15")
extractPDFPageNoDetailsLabel.place(x=175, y=10, anchor="w")


extractPDFSourceLabel = Label(extractPDFConvert, text="Source")
extractPDFSourceLabel.place(x=5, y=40, anchor="w")
extractPDFSourceEntry = Entry(extractPDFConvert,width=69,textvariable=extractPDF_folder_path)
extractPDFSourceEntry.place(x=75,y=40,anchor="w")
extractPDFSourceButton=Button(extractPDFConvert,text="Browse",command=browse_extractPDF_source_button)
extractPDFSourceButton.place(x=500,y=40,anchor="w")

extractPDFDestinationLabel = Label(extractPDFConvert, text="Destination")
extractPDFDestinationLabel.place(x=5, y=70, anchor="w")
extractPDFDestinationEntry = Entry(extractPDFConvert,width=69,textvariable=extractPDF_dest_folder_path)
extractPDFDestinationEntry.place(x=75,y=70,anchor="w")
extractPDFDestinationButton=Button(extractPDFConvert,text="Browse",command=browse_extractPDF_destination_button)
extractPDFDestinationButton.place(x=500,y=70,anchor="w")
 
extractPDFButton = Button(tab4,text="  Extract Page From PDF File  ",command=extractPageFromPDF)
extractPDFButton.place(x=210,y=140,anchor="w")
#****************************************************************************************

tabcontrol.pack(expand="5", fill="both")

'''
errorArea = LabelFrame(root, text=" Errors ", width=600, height=80)
errorArea.grid(row=2, column=0, columnspan=2, sticky="E", \
             padx=100, pady=0, ipadx=0, ipady=0)
errorArea.place(x=50,y=250)
errorMessage = Label(errorArea, text="hello")
errorMessage.place(x=100, y=40, anchor="w")
'''

root.deiconify()
root.mainloop()