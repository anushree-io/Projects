
import sys
import os
import time
import schedule
import shutil
import hashlib
import zipfile

def make_zip(folder):
    timestamp =time.strftime("%Y-%m-%d_%H-%M-%S")

    zip_name = folder + "_" + timestamp + ".zip"

    # Open the zip file
    zobj = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)

    for root,dirs,files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root,file)
            relative = os.path.relpath(full_path,folder)

            zobj.write(full_path,relative)
    zobj.close()
    return zip_name

def Calculate_hash(path):

    hobj = hashlib.md5()

    fobj = open(path, "rb")

    while True:
        data = fobj.read(1024)
        if not data:
            break
        else:
            hobj.update(data)

    fobj.close()

    return hobj.hexdigest()

def BackupFiles(Source,Destination):
    copied_files = []

    print("Creating the Backup Foler for Backup Process.")

    os.makedirs(Destination, exist_ok = True)

    for root,dirs,files in os.walk(Source):
        for file in files:
            src_path = os.path.join(root,file)

            relative = os.path.relpath(src_path,Source)
            dest_path = os.path.join(Destination,relative)

            os.makedirs(os.path.dirname(dest_path), exist_ok = True)

            # Copy the files if its new 
            if ((not os.path.exists(dest_path)) or (Calculate_hash(src_path) != Calculate_hash(dest_path))):
                shutil.copy2(src_path,dest_path)
                copied_files.append(relative)
    
    return copied_files

def MarvellousDataShieldStart(Source = "Data"):
    Border = "_"*50
    BackupName = "MarvelloudBackup"
    
    print(Border) 
    print("Backup Process Started Successfully at: ", time.ctime())
    print(Border) 

    files = BackupFiles(Source, BackupName)

    print(Border) 
    zip_file = make_zip(BackupName)
    print("Backup Completed Successfully")
    print("Files Copied: ", len(files))
    print("Zip files gets created:",zip_file)


def main():

    Border = "_"*50
    print(Border) 
    print("------------ Marvellous Data Shield Syatem ----------")
    print(Border)

    if len(sys.argv) == 2 :
        if sys.argv[1] == "--h" or sys.argv[1] == "--H":
             print("This script is used to:")
             print("1: Takes auto backup at given time")
             print("2: Backup only new and updated files")
             print("3: Create an archive of the backup periodically")


        elif sys.argv[1] == "--u" or sys.argv[1] == "--U":
            print("Use the automation script as")
            print("ScriptName.py Time Interval SourceDirectory")
            print("TimeInterval: The time in minites for periodic scheduling")
            print("SourceDirectory: Name of directory to be backed up")

        else:
            print("Unabe to proceed as there is no such option")
            print("Please udse --h or -- u to get more details")

     # python Demo.py 5 Data   
    elif len(sys.argv) == 3:
        print("Inside Projects logic")
        print("Time Interval:",sys.argv[1])
        print("Directory Name:",sys.argv[2])
        
        # Apply the scheduler
        schedule.every(int(sys.argv[1])).minutes.do(MarvellousDataShieldStart),sys.argv[2]
        
        print(Border) 
        print("Data Shield System started Successfully")
        print("Time Interval in minutes:",sys.argv[1])
        print("Press Ctrl + C to stop the execution")

        # Wait till abort
        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        print("Invalid number of command line arguments")
        print("Unabe to proceed as there is no such option")
        print("Please udse --h or -- u to get more details")


    print(Border)
    print("---------- Thank You for using our Script ----------")
    print(Border)

if __name__ == "__main__":
    main()