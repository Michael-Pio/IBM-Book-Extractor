import os
from time import sleep
import adb_control as ac
import binary_control as BIN
import PIL.Image as PIMG

class IBM_Scrapper:
    MemuPath = "/storage/emulated/0/Project_X/screenCapture/IOT/" 
    NetWorkWaitTime = 4 #in Seconds
    NextPos = (990,350)
    (left,upper,right,lower) = (0,334,1080,1734)

    def ProgressBar(self,percentage:int,ProgressName:str):
        value = percentage
        print(f"[{ProgressName}]"+"  :"+"#"*(value) + "."*((100-value))+f"  {percentage}%")

    def __init__(self,UnitName,StartPage,TotPage):
        self.StartPage = StartPage
        self.TotPage = TotPage
        self.UnitName = UnitName
        self.DevicePath = "IBM_BOOKS/IOT/pic/"+self.UnitName+"/"
        print("Begining the Operation :")
        print("[operation]  Capturing Images Begins")
        self.CaptureScreenShot()
        print("[operation]  screenshot Captured succesfully !")
        print("[operation]  Importing Image Begins")
        self.ImportImage()
        print("[operation]  Images Imported Succesfully")
        print("[operation]  Croping Image Begins")
        self.CropImage()
        print("[operation]  Croping images Ends ")

    def CaptureScreenShot(self):
        #Capturing the ScreenShots 
        i = int(input("Enter 0 \tto skip or \t1 to CaptureScreenshot :"))
        if(i == 1):
            ind = 0
            tot = self.TotPage - self.StartPage
            for i in range(self.StartPage,self.TotPage+1):
                ind +=1
                sleep(2)
                ac.ADB_screencap(self.UnitName+"page"+str(i),self.MemuPath)
                ac.ADB_tap(self.NextPos[0],self.NextPos[1])
                sleep(4)
                percent = int((ind/tot) * 100)
                self.ProgressBar(percent,"Capturing IMG")

    def ImportImage(self):
        i = int(input("Enter \t0 to skip or \t1 to Import Images:"))
        if(i == 1):
            ind = 0
            tot = self.TotPage - self.StartPage
            #Getting Images from The Emulator
            for i in range(self.StartPage,self.TotPage+1):
                ac.ADB_pull(self.MemuPath+self.UnitName+"page"+str(i)+".png",self.DevicePath)
                sleep(0.2)
                ind+=1
                percent = int((ind/tot)* 100)
                self.ProgressBar(percent,"Importing IMG")

    def CropImage(self):
        i = int(input("Enter \t0 to skip or \t1 to Crop Images :"))
        if(i == 1):
            #Croping Image
            TotalFiles = len(os.listdir(self.DevicePath))
            ind = 0
            for i in os.listdir(self.DevicePath):
                self.file = f"{self.DevicePath}\\{i}"
                img = PIMG.open(self.file)
                img = img.crop((self.left,self.upper,self.right,self.lower))
                img.save(self.file)
                ind+=1
                percent:int = int((ind/TotalFiles)*100)
                self.ProgressBar(percent,"Croping IMG")


BIN.launchLiveLogDisplayer()
# BIN.launchMemu()
sleep(5)
ac.ADB_KillServer()
ac.ADB_startServer()
sleep(5)
ac.ADB_listDevices()
ac.ADB_connectMemu()


I = IBM_Scrapper("Unit5",1,130)
