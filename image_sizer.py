from PIL import Image, ImageDraw, ImageFont #pip install pillow
import os, sys
import argparse  #pip install argparse

result_list = []

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

            # check to see if it is a valid file and if it is a supported image type
            if os.path.isfile(full_file_path) and e in ['.jpg', '.png', '.gif', '.webp', '.bmp']:

                #hand file to resize
                resize(full_file_path, args.width, args.watermark, args.color)            

    #if we are doing a file
    elif args.file != "":

        #get file        
        item = args.file

        #split the extension off
        f, e = os.path.splitext(item.lower())

        #check if it is a file and if it is a valid image extension
        if os.path.isfile(item) and e in ['.jpg', '.png', '.gif', '.webp', '.bmp']:

            #hand file to resize
            resize(args.file, args.width, args.watermark, args.color)            
            
    #no good params
    else:
        print("no file or dir path given.")
        quit()
    
    print("Successfully created the following files")
    for file in result_list:
        print(file)

#resize a file given the widths provided
def resize(file, widths, watermarks, color):

    index = 0

    for width in widths:

        #generate save name and save, replacing spaces with underscores if needed.
        # get the path and file name
        path, file_name = os.path.split(file)
        
        # split off the file extension off the file name
        file_name_no_ext, file_extension = os.path.splitext(file_name)

        # make it lower case, and replace spaces
        file_name_no_ext = file_name_no_ext.lower().replace(" ","_")

        #put the path back together
        full_path = os.path.join(path,file_name_no_ext)
        save_name = ''.join([full_path, "_", str(width), file_extension])

        #open file
        img = Image.open(file)

        # calculate height
        height = int(img.height * (width / img.width))

        # resize the image
        img = img.resize((width ,height), Image.Resampling.LANCZOS)

        #if watermark
        if len(watermarks) == 1:
            #watermark the image
            img = watermark_image_with_text(img, watermarks[0], color)

        elif len(watermarks) == len(widths):
            #watermark the image
            img = watermark_image_with_text(img, watermarks[index], color)

            #increment the watermark index
            index +=1

        #else we don't do any watermarking
        else:
            pass

        img.save(save_name)         
        result_list.append(save_name)


def watermark_image_with_text(image: Image, watermark: str, color: str):
    
    #create the watermark image
    imageWatermark = Image.new("RGBA", image.size, (255, 255, 255, 0))
    
    #set up font
    font_family = 'arial.ttf'
    width, height = image.size
    draw = ImageDraw.Draw(imageWatermark)
    font = ImageFont.truetype(font_family, int(height / 18))

    #set up location
    textWidth, textHeight = draw.textsize(watermark, font)
    x = width - textWidth - 5
    y = height - textHeight -5

    #draw text
    draw.text((x, y), watermark, color, font)

    #convert the current image to RGBA so that we can alpha composite
    temp_image = image.convert("RGBA")

    #composite
    new_image =  Image.alpha_composite(temp_image, imageWatermark)

    #put it back in the correct mode
    final_image = new_image.convert(image.mode)

    #return the new image
    return final_image


if __name__ == "__main__":

    parser = argparse.ArgumentParser(epilog= "\
    EXAMPLE calls:\n\
\
        image_sizer.py -path c:\\github\\myproject\\images -width 300 600 900\n\
        image_sizer.py -file c:\\github\\myproject\\images\\foobar.jpg -width 400 800 -watermark medium large -color blue", 
        formatter_class=CustomFormatter)
    parser.add_argument("-path", type=str, default="", help="path to directory of images to be resized.")
    parser.add_argument("-file", type=str, default ="", help="path to a single file to be resized.")
    parser.add_argument('-width', type=int, nargs="*", default = [200,400,600], help="list of widths to resize the image(s). height will be calculated to maintain aspect ratio." )
    parser.add_argument('-color',type=str, default="white", help="optional color name for the watermark(s). Defaults to white")
    parser.add_argument('-watermark', type=str, nargs="*", default = '',help="optional text string for watermarking images. If one value, it will be applied to all. if more than one, should be the same number as number of widths")
    
    

    args = parser.parse_args()

    main(args)
    

