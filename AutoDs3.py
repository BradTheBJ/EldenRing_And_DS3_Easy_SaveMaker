import os
import shutil

path = 'C:\\Users\\benjo\\AppData\\Roaming\\DarkSoulsIII\\01100001135b0a20\\ds30000.sl2'
destination_dir = 'D:\\Temporary Souls Like Save Files'
sub_dir = os.path.join(destination_dir, 'Dark Souls III Save File')
destination_file = os.path.join(sub_dir, 'ds30000.sl2')

if os.path.exists(path):
    print("file exists")
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    shutil.copyfile(path, destination_file)
    print(f"File copied to {destination_file}")
else:
    print("file not found")