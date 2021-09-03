from PIL import Image
import io

inputFile = "Example Files\\Bonk.gif"
outputFile = "Output\\Bonk.h"
outputPic = "Output\\Pictures\\Bonk"
name = "Bonk"

class Frame:
    data = []

frameNames = []
frames = []
palette = []
w = 0
h = 0

def GetFrames(image):
    global palette, w, h

    w, h = image.size
    frameCount = image.n_frames

    for x in range(frameCount):
        image.seek(x)

        rgbData = []

        for i in range(h):
            for j in range(w):
                index = image.getpixel((j, i))

                rgbData.append(index)

        frame = Frame()
        frame.rgbData = rgbData
        frames.append(frame)
        
        image.save(outputPic + str(x) + ".png")

def GetImageSequence(image, className):
    frameCount = image.n_frames
    
    data = "#pragma once\n\n"
    data += "#include \"..\..\Animation\ImageSequence.h\"\n\n"

    data += "class " + className + "Sequence : public ImageSequence{\n"
    data += "private:\n"

    for i in range(len(frames)):
        data += "\tstatic const uint8_t frame" + str(i).rjust(4, '0') + "[];\n"

    data += "\n"

    data += "\tstatic const uint8_t* sequence[" + str(frameCount) + "];\n\n"
    
    data += "\tstatic const uint8_t rgbColors[];\n\n"

    data += "\tImage image = Image(frame0000, rgbColors, " + str(w) + ", " + str(h) + ", "  + str(int(len(palette) / 3) - 1) + ");\n\n"
    data += "public:\n"
    data += "\t" + className + "Sequence(Vector2D size, Vector2D offset, float fps) : ImageSequence(&image, sequence, (unsigned int)" + str(frameCount) + ", fps) {\n"
    data += "\t\timage.SetSize(size);\n"
    data += "\t\timage.SetPosition(offset);\n"
    data += "\t}\n"
    
    data += "};\n\n"
    
    for i, frame in enumerate(frames):
        data += "const uint8_t " + className + "Sequence::frame" + str(i).rjust(4, '0') + "[] PROGMEM = {"

        for j, frameData in enumerate(frame.rgbData):
            data += str(frameData)
            
            if j + 1 != len(frame.rgbData):
                data += ","
            else:
                data += "};\n"

    data += "\nconst uint8_t* " + className + "Sequence::sequence[] = {"

    for i, frame in enumerate(frames):
        data += "frame" + str(i).rjust(4, '0')
        
        if i + 1 != len(frames):
            data += ","
        else:
            data += "};\n"

    data += "const uint8_t " + className + "Sequence::rgbColors[] PROGMEM = {"

    for i in range(int(len(palette) / 3)):
        r = palette[i * 3]
        g = palette[i * 3 + 1]
        b = palette[i * 3 + 2]

        data += str(r) + "," + str(g) + "," + str(b)
        
        if i == len(palette) / 3 - 1:
            data += "};\n"
        else:
            data += ","

    return data


image = Image.open(inputFile)

image.seek(0)

palette = image.getpalette()

print("Number of frames: " + str(image.n_frames))
print("Number of palette colors: " + str(int(len(palette) / 3)))

GetFrames(image)#parse frame data

output = GetImageSequence(image, name)

print(output)
f = open(outputFile, "w")
f.write(output)
f.close()
