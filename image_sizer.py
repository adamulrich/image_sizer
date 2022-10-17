from PIL import Image #pip install pillow
import os
import argparse  #pip install argparse

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

def main(args):

    #if we are doing a directory
    path = args.path
    if path != "":
        
        #walk the items in the directory
        dirs = os.listdir(path)
        for item in dirs:
            
            #get the file name and extension, make sure everything is lower case
            f, e = os.path.splitext(item.lower())
            full_file_path = (os.path.join(path,item)).lower()
            if os.path.isfile(full_file_path) and e in ['.jpg', '.png', '.gif', '.webp', '.bmp']:
                #hand file to resize
                resize(full_file_path,args.width)            

    #if we are doing a file
    elif args.file != "":
        resize(args.file,args.width)            

    #no good params
    else:
        print("no file or dir path given.")

#resize a file given the widths provided
def resize(file, widths):

    for width in widths:

        #open file
        img = Image.open(file)

        # $todo calculate height
        height = int(img.height * (width / img.width))

        img = img.resize((width ,height), Image.Resampling.LANCZOS)
        
        #generate save name and save, replacing spaces with underscores if needed.
        f, e = os.path.splitext(file)
        save_name = ''.join([f, "_", str(width), e]).lower().replace(" ","_")
           
        img.save(save_name) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog= "EXAMPLE calls:\nimage_sizer.py -path c:\\github\\myproject\\images -width 300 600 900\nimage_sizer.py -file c:\\github\\myproject\\images\\foobar.jpg -width 400 800", 
        formatter_class=CustomFormatter)
    parser.add_argument("-path", type=str, default="", help="path to directory of images to be resized.")
    parser.add_argument("-file", type=str, default ="", help="path to a single file to be resized.")
    parser.add_argument('-width', type=int, nargs="*", default = [200,400,600], help="list of widths to resize the image(s). height will be calculated to maintain aspect ratio." )
    args = parser.parse_args()
    main(args)
    

