from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from pypdf import PdfReader, PdfWriter, PdfMerger
import os
import subprocess
import img2pdf
from PIL import Image
import sys

iMaxStackSize = 5000
sys.setrecursionlimit(iMaxStackSize)

def browse_split_source_button():
    global split_folder_path
    filename = filedialog.askopenfilename(initialdir = last_opened_source_path.get(),title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))    
    last_opened_source_path.set(os.path.dirname(filename))
    split_folder_path.set(filename)
    #print(split_folder_path.get())
    #print(os.path.dirname(folder_path.get()))

def browse_split_destination_button():
    global split_des_folder_path
    filename=filedialog.askdirectory(initialdir = last_opened_dest_path.get())
    last_opened_dest_path.set(filename)   
    split_des_folder_path.set(filename)
    #print(split_des_folder_path.get())
    
def splitToPDF():
 
    try:
        #print(split_des_folder_path.get())
        inputpdf = PdfReader(open(split_folder_path.get(), "rb"),strict=False)
        i=0
        for pages in inputpdf.pages:
            output = PdfWriter()
            output.add_page(pages)
            i=i+1
            with open(split_des_folder_path.get() + "/pdfpage%02d.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
    
        messagebox.showinfo("Info","PDF File Splitted Successfully")
        subprocess.run(['explorer', os.path.realpath(split_des_folder_path.get())])
    except:
      messagebox.showerror("Warning","Some Error Occured")
    finally:
       split_folder_path.set("")
       split_des_folder_path.set("")

def browse_merge_sourcefolder_button():
    global merge_folder_path
    filename = filedialog.askdirectory(initialdir = last_opened_source_path.get())  # askdirectory()
    last_opened_source_path.set(filename)
    merge_folder_path.set(filename)

def browse_merge_source_button():
    filename = filedialog.askopenfilenames(initialdir = last_opened_source_path.get(), title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_source_path.set(filename)
    merge_folder_path.set(filename)

    for fname in filename:
        multiple_file_names.append(fname)    
  
def browse_merge_destination_button():
    global merge_des_folder_path
    filename=filedialog.asksaveasfilename(initialdir = last_opened_dest_path.get(),title = "Save file",defaultextension="*.pdf",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_dest_path.set(os.path.dirname(filename))
    merge_des_folder_path.set(filename)
    #messagebox.showinfo("file name", merge_des_folder_path.get())

def radioMergePDF():
    if mvalue.get() == 1:
        browse_merge_sourcefolder_button()
    elif mvalue.get() == 2:
        browse_merge_source_button()

def mergePDFByFolder():
    try:
        x = [os.path.abspath(os.path.join(merge_folder_path.get(), a)) for a in os.listdir(merge_folder_path.get()) if a.endswith(".pdf")]
        merger = PdfMerger()

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

def mergePDFByMultipleFiles():
    try:       
        merger = PdfMerger()
        for pdf in multiple_file_names:            
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
        multiple_file_names.clear()     
       
def mergeToPDF():
    if mvalue.get() == 1:
        mergePDFByFolder()
    elif mvalue.get() == 2:
        mergePDFByMultipleFiles()     

def browse_img2pdf_source_button():
    global img2pdf_folder_path
    if(rvalue.get()==1):
        filename = filedialog.askopenfilename(initialdir = last_opened_source_path.get(),title = "Select file",filetypes = \
                    (("jpg files","*.jpg"),("all files","*.*")))        
        last_opened_source_path.set(os.path.dirname(filename))
    else:
        filename = filedialog.askdirectory(initialdir = last_opened_source_path.get())  # askdirectory()
        last_opened_source_path.set(filename)
    img2pdf_folder_path.set(filename)

def browse_img2pdf_destination_button():
    global img2pdf_dest_folder_path
    if(rvalue.get() == 2):
        filename = filedialog.askdirectory(initialdir = last_opened_dest_path.get())  # askdirectory()
        last_opened_dest_path.set(filename)
    elif(rvalue.get() == 3 or rvalue.get() == 1):
        filename = filedialog.asksaveasfilename(initialdir = last_opened_dest_path.get(),title = "Save file",defaultextension="*.pdf",filetypes = \
                    (("pdf files","*.pdf"),("all files","*.*")))
        last_opened_dest_path.set(os.path.dirname(filename))
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
    merger = PdfMerger()
    
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
    filename = filedialog.askopenfilename(initialdir = last_opened_source_path.get(),title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_source_path.set(os.path.dirname(filename))
    extractPDF_folder_path.set(filename)

def browse_extractPDF_destination_button():
    global extractPDF_dest_folder_path
    filename=filedialog.asksaveasfilename(initialdir = last_opened_dest_path.get(),title = "Save file",defaultextension="*.pdf",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_dest_path.set(os.path.dirname(filename))
    #filename=filedialog.askdirectory()
    extractPDF_dest_folder_path.set(filename)
 
def extractPageFromPDF():
    try:

        #print(getPDFPageNumber(extractPDFPageNumber.get()))
        pageNumber = getPDFPageNumber(extractPDFPageNumber.get())
        output = PdfWriter()
        inputpdf = PdfReader(open(extractPDF_folder_path.get(), "rb"),strict=False)
        
        i=0
        for page in inputpdf.pages:
            if((i+1) in pageNumber):
                output.add_page(page)
            i = i + 1

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
  
def browse_compress_source_button():
    global compress_folder_path
    filename = filedialog.askopenfilename(initialdir = last_opened_source_path.get(),title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_source_path.set(os.path.dirname(filename))
    compress_folder_path.set(filename)
    #print(split_folder_path.get())
    #print(os.path.dirname(folder_path.get()))

def browse_compress_destination_button():
    global compress_des_folder_path
    filename=filedialog.asksaveasfilename(initialdir = last_opened_dest_path.get(),title = "Save file",defaultextension="*.pdf",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_dest_path.set(os.path.dirname(filename))
    compress_des_folder_path.set(filename)

def compressPDFQualityOnOff():
    if checkButtonValue.get():
        compressPageQualityEntry.config(state= "disabled")   
        compress_PDF_Quality.set(0)     
    else:     
        compressPageQualityEntry.config(state= "enabled")
    
def compressToPDF():
    try:
        inputpdf = PdfReader(open(compress_folder_path.get(), "rb"),strict=False)
        output = PdfWriter()
        for page in inputpdf.pages:            
            output.add_page(page)

        if checkButtonValue.get():
            for page in output.pages:
                page.compress_content_streams()      
        else:   
            for page in output.pages:
                for img in page.images:
                    img.replace(img.image, quality=compress_PDF_Quality.get())        
            
        with open(compress_des_folder_path.get(), "wb") as outputStream:
            output.write(outputStream)
        
        messagebox.showinfo("Info","PDF File Compressed Successfully")
        subprocess.run(['explorer', os.path.realpath(compress_des_folder_path.get())])
    except:
        messagebox.showerror("Warning","Some Error Occured")
    finally:    
        compress_folder_path.set("")
        compress_des_folder_path.set("")

def browse_insdel_source_button():
    filename = filedialog.askopenfilename(initialdir = last_opened_source_path.get(),title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_source_path.set(os.path.dirname(filename))
    insDel_src_folder_path.set(filename)
    
def browse_insdel_destination_button():    
    filename=filedialog.asksaveasfilename(initialdir = last_opened_dest_path.get(),title = "Save file",defaultextension="*.pdf",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_dest_path.set(os.path.dirname(filename))
    insDel_des_folder_path.set(filename)

def browse_insdel_inspage_button():
    filename = filedialog.askopenfilename(initialdir = last_opened_source_path.get(),title = "Select file",filetypes = \
                                        (("pdf files","*.pdf"),("all files","*.*")))
    last_opened_source_path.set(os.path.dirname(filename))
    insDel_page_folder_path.set(filename)

def radioInsDelPDFFiles():
    if(idvalue.get() == 1):
        insDelInsPageLabel.config(state= "disabled")  
        insDelInsPageEntry.config(state= "disabled")  
        insDelInsertSourceButton.config(state= "disabled")  
    elif(idvalue.get() == 2):
        insDelInsPageLabel.config(state= "enabled")  
        insDelInsPageEntry.config(state= "enabled")  
        insDelInsertSourceButton.config(state= "enabled") 
    
def insDelPDFFiles():
    if(idvalue.get() == 1):
        deletePDFFiles()    
    elif(idvalue.get() == 2):     
        insertPDFFiles()

    insDel_src_folder_path.set("") 
    insDel_des_folder_path.set("")
    insDel_page_folder_path.set("")           

def insertPDFFiles():
    messagebox.showinfo("","insert")

def deletePDFFiles():
    messagebox.showinfo("","detele")


#This section initiate Graphics and defines position and geometry of windows which opens
root =Tk()
root.title("Welcome to PDF Splitter/Merger                        Developed By: Deepak Kumar Ram")
#root.iconbitmap(r"C:\Users\Deepak\Desktop\Installer\sbi.ico")
# #root.overrideredirect(1)

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
tabcontrol.add(tab1,text=" PDF Splitter ")

# This section for Tab1 PDF Splitter ***************************************************
split_folder_path = StringVar()
split_des_folder_path=StringVar()
last_opened_source_path = StringVar()
last_opened_dest_path = StringVar()

desktop = os.path.expanduser("~/Desktop")
last_opened_source_path.set(desktop)
last_opened_dest_path.set(desktop)

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
tabcontrol.add(tab2,text=" PDF Merger ")

# This section for Tab2 PDF Merger ***************************************************
merge_folder_path = StringVar()
merge_des_folder_path=StringVar()
mvalue = IntVar()
mvalue.set(1)
pdfMerge = LabelFrame(tab2, text=" Merger Multiple PDF Files to Single File ", width=585, height=110)
pdfMerge.place(x=10,y=10)

mergeByFolderRadio =Radiobutton(pdfMerge, text = "Merge By Folder", variable=mvalue, value=1)
mergeByFolderRadio.place(x=70, y=14, anchor=W)
mergeByMultipleFileRadio = Radiobutton(pdfMerge,text="Merge By Multiple Files", variable=mvalue, value=2)
mergeByMultipleFileRadio.place(x=187, y=14, anchor=W)

mergeSourceLabel = Label(pdfMerge, text="Source")
mergeSourceLabel.place(x=5, y=40, anchor="w")
mergeSourceEntry = Entry(pdfMerge,width=70,textvariable=merge_folder_path)
mergeSourceEntry.place(x=70,y=40,anchor="w")
mergeSourceButton=Button(pdfMerge,text="Browse",command=radioMergePDF)
mergeSourceButton.place(x=500,y=40,anchor="w")

mergeDestinationLabel = Label(pdfMerge, text="Destination")
mergeDestinationLabel.place(x=5, y=70, anchor="w")
mergeDestinationEntry = Entry(pdfMerge,width=70,textvariable=merge_des_folder_path)
mergeDestinationEntry.place(x=70,y=70,anchor="w")
mergeDestinationButton=Button(pdfMerge,text="Browse",command=browse_merge_destination_button)
mergeDestinationButton.place(x=500,y=70,anchor="w")

mergePDFButton = Button(tab2,text="  Merge PDF Files  ",command=mergeToPDF)
mergePDFButton.place(x=250,y=140,anchor="w")
#****************************************************************************************

tab3 = Frame(tabcontrol)
tabcontrol.add(tab3,text=" Image to PDF ")

#This Section is for Tab3 Image to PDF *****************************************************
rvalue=IntVar()
img2pdf_dest_folder_path=StringVar()
img2pdf_folder_path=StringVar()
rvalue.set(1)
multiple_file_names=[]

imagePDFMergeConvert = LabelFrame(tab3, text=" Convert Image Files to PDF Files ", width=585, height=110)
imagePDFMergeConvert.place(x=10,y=10)

imageSingleToPDFRadio =Radiobutton(imagePDFMergeConvert, text = "Single File to PDF", variable=rvalue, value=1)
imageSingleToPDFRadio.place(x=70, y=14, anchor=W)
imageToPDFRadio = Radiobutton(imagePDFMergeConvert,text="All Image to Seperate PDF", variable=rvalue, value=2)
imageToPDFRadio.place(x=187, y=14, anchor=W)
imageToPDFMergeRadio = Radiobutton(imagePDFMergeConvert,text="All Image to PDF and Merge", variable=rvalue, value=3)
imageToPDFMergeRadio.place(x=350, y=14, anchor=W)

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
tabcontrol.add(tab4,text=" Extract PDF Page ")

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

tab5 = Frame(tabcontrol)
tabcontrol.add(tab5,text=" Compress PDF Page ")
compress_folder_path = StringVar()
compress_des_folder_path=StringVar()
compress_PDF_Quality = IntVar()

pdfCompress = LabelFrame(tab5, text=" Compress File ", width=585, height=110)
pdfCompress.place(x=10,y=10)

checkButtonValue = IntVar()
checkButtonValue.set(1)
compressChkPageQualityOnOFF = Checkbutton(pdfCompress,text="Page Quality",variable=checkButtonValue,onvalue=0,offvalue=1,  command=compressPDFQualityOnOff)
compressChkPageQualityOnOFF.place(x=70, y=10, anchor="w")
compressPageQualityEntry = Entry(pdfCompress,width=15,state="disabled",textvariable=compress_PDF_Quality)
compressPageQualityEntry.place(x=165,y=10,anchor="w")

compressSourceLabel = Label(pdfCompress, text="Source")
compressSourceLabel.place(x=5, y=40, anchor="w")
compressSourceEntry = Entry(pdfCompress,width=70,textvariable=compress_folder_path)
compressSourceEntry.place(x=70,y=40,anchor="w")
compressSourceButton=Button(pdfCompress,text="Browse",command=browse_compress_source_button)
compressSourceButton.place(x=500,y=40,anchor="w")

compressDestinationLabel = Label(pdfCompress, text="Destination")
compressDestinationLabel.place(x=5, y=70, anchor="w")
compressDestinationEntry = Entry(pdfCompress,width=70,textvariable=compress_des_folder_path)
compressDestinationEntry.place(x=70,y=70,anchor="w")
compressDestinationButton=Button(pdfCompress,text="Browse",command=browse_compress_destination_button)
compressDestinationButton.place(x=500,y=70,anchor="w")

convertPDFButton = Button(tab5,text="  Compress PDF  ",command=compressToPDF)
convertPDFButton.place(x=250,y=140,anchor="w")
#****************************************************************************************

tab6 = Frame(tabcontrol)
tabcontrol.add(tab6,text=" Insert/Delete Page ")
insDel_src_folder_path = StringVar()
insDel_des_folder_path=StringVar()
insDel_page_folder_path = StringVar()
insDel_PDF_No = IntVar()
idvalue =IntVar()
idvalue.set(1)

pdfInsertDelete = LabelFrame(tab6, text=" Insert/Delete Page From File ", width=585, height=110)
pdfInsertDelete.place(x=10,y=10) 

insDelLabel = Label(pdfInsertDelete, text="Page No")
insDelLabel.place(x=5, y=14, anchor="w")
insDelLabelPageNoEntry = Entry(pdfInsertDelete,width=8,textvariable=extractPDFPageNumber)
insDelLabelPageNoEntry.place(x=70,y=14,anchor="w")

deleteRadio = Radiobutton(pdfInsertDelete,text="Delete Page", variable=idvalue, value=1,command=radioInsDelPDFFiles)
deleteRadio.place(x=130, y=14, anchor=W)
insertRadio =Radiobutton(pdfInsertDelete, text = "Insert Page", variable=idvalue, value=2,command=radioInsDelPDFFiles)
insertRadio.place(x=215, y=14, anchor=W)

insDelInsPageLabel = Label(pdfInsertDelete, text="Inserted Page", state="disabled")
insDelInsPageLabel.place(x=310, y=14, anchor="w")
insDelInsPageEntry = Entry(pdfInsertDelete,width=16,textvariable=insDel_page_folder_path, state="disabled")
insDelInsPageEntry.place(x=390,y=14,anchor="w")
insDelInsertSourceButton=Button(pdfInsertDelete,text="Browse", state="disabled", command=browse_insdel_inspage_button)
insDelInsertSourceButton.place(x=500,y=14,anchor="w")

insDelSourceLabel = Label(pdfInsertDelete, text="Source")
insDelSourceLabel.place(x=5, y=42, anchor="w")
insDelSourceEntry = Entry(pdfInsertDelete,width=70,textvariable=insDel_src_folder_path)
insDelSourceEntry.place(x=70,y=42,anchor="w")
insDelSourceButton=Button(pdfInsertDelete,text="Browse",command=browse_insdel_source_button)
insDelSourceButton.place(x=500,y=42,anchor="w")

insDelDestinationLabel = Label(pdfInsertDelete, text="Destination")
insDelDestinationLabel.place(x=5, y=70, anchor="w")
insDelDestinationEntry = Entry(pdfInsertDelete,width=70,textvariable=insDel_des_folder_path)
insDelDestinationEntry.place(x=70,y=70,anchor="w")
insDelDestinationButton=Button(pdfInsertDelete,text="Browse",command=browse_insdel_destination_button)
insDelDestinationButton.place(x=500,y=70,anchor="w")

insDelPDFButton = Button(tab6,text="  Insert / Delete Page  ",command=insDelPDFFiles)
insDelPDFButton.place(x=250,y=140,anchor="w")

tabcontrol.pack(expand="7", fill="both")

root.deiconify()
root.mainloop()
