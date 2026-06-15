import os
import sys
import time
import schedule

def DirectoryScanner(DirName = "Marvellous"):            # Default directory name
    Border = "-" * 50 
    timestamp = time.ctime()                             # Current time stamp

    LogFileName = "Marvellous%s.log" %(timestamp)        # Create log file name with time stamp ; %s is placeholder for string
    LogFileName = LogFileName.replace(" ","_")           # Replace space with _
    LogFileName = LogFileName.replace(":","_")           # Replace : with _

    fobj = open(LogFileName,"w")                         # Open log file in write mode

    
    fobj.write(Border + "\n")
    fobj.write("This is a log file created by Mavellous Automation \n")
    fobj.write("This is a Directory Cleaner Script\n")
    fobj.write(Border + "\n")

    Ret = False

    Ret = os.path.exists(DirName)                              # Check whether directory exists
    if (Ret == False):                                         
        print("There is no such directory.")
        return
    
    Ret = os.path.isdir(DirName)                             # Check whether it is a directory
    if (Ret == False):
        print("It is not a directory")

    FileCount = 0
    EmptyFileCount = 0

    for FolderName, SubFolder,FileName in os.walk(DirName):    # Traverse through directory
        
        for fname in FileName:                                 # Iterate each file
            FileCount = FileCount + 1                          # Increment file count

            fname = os.path.join(FolderName,fname)             # Create full path of file

            if (os.path.getsize(fname) == 0) :                 # Empty file   # Check whether file size is zero
                EmptyFileCount = EmptyFileCount + 1            # Increment empty file count
                os.remove(fname)    

    
    fobj.write("Total files scanned :" +str(FileCount)+"\n")          # Write total files scanned to log file, typecast int to str because write function accepts string only
    fobj.write("Total Empty Files found:" +str(EmptyFileCount)+"\n")    
    fobj.write("This log file is created at: " +timestamp+"\n" )
    fobj.write(Border + "\n")  

    fobj.close()
        
    
def main():
    Border = "-" * 50
    print(Border)
    print("---------Marvellous Directory Automation----------")
    print(Border)

    if (len(sys.argv) != 2):                                       # Check for command line arguments
        print("Invalid number of arguments")
        print("Please specify the name of directory")
        return
    
    # DirectoryScanner(sys.argv[1])                         # Call DirectoryScanner function with directory name provided by user
    schedule.every(1).minute.do(DirectoryScanner)           # Schedule the DirectoryScanner function to run every minute

    while True:                                             # Infinite loop to keep the scheduler running
        schedule.run_pending()                              # Run pending scheduled tasks
        time.sleep(1)

    print(Border)
    print("---------Marvellous Directory Automation----------")
    print(Border)
   
if __name__ == "__main__":
    main()