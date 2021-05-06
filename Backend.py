import numpy 
from numpy import asarray
from PIL import Image,ImageOps



def hide(pixel,msg):
    #8 bit Slicing 
    bno='{:08b}'.format(pixel) #pixel value to 8 bit binary
    #print(bno)
    no=bno[:-1]+msg # Replacing the LSB with the data bit to be encoded
    #print(no)
    #Converting number from binary to integer
    ans= int(no,2)
    #print(ans)
    return ans

def unhide(pixel):
    #bno='{:08b}'.format(pixel)
    bno= bin(pixel)
    return bno[-1]


    
def BinaryToDecimal(binary):  
         
    binary1 = binary  
    decimal, i, n = 0, 0, 0
    while(binary != 0):  
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)  
        binary = binary//10
        i += 1
    return (decimal)     
    

def encode(image1,msg):
    image1=image1.convert('RGB')
    
    mywidth = 256
    
    wpercent = (mywidth/float(image1.size[0])) 
    hsize = int((float(image1.size[1])*float(wpercent)))
    image1 = image1.resize((mywidth,hsize))
    #Compressing the Image such that the width is always 256 
    #Without changing the ratio of the image (Only resolution is changed)
    #Get new image dimensions
    r,c=image1.size[0],image1.size[1]
    #print(r,c)
    #Covert to Grayscale
    #image2=ImageOps.grayscale(image1)
    #print(image2.size)
    #Covert to a numpy array
    data=asarray(image1)
    print(data)
    #print(data)
    #Covert to list
    data1=data.tolist()
    #print(data1)
    #image2.show()
    #Add a key to the message 
    msg = "wearempstmemomoteam"+msg+"$$$"
    x=''
    for i in msg:
        x+=format(ord(i), '08b') #Convert String -> Charectors -> ASCII -> 8bit binary

    #x= ' '.join(format(ord(i), 'b') for i in msg) 
    #print(x)
    x=str(x) #String of binary
    #print(x)
    arr = data1 #Copy of image array
    #print(len(data1))
    ctr=0 #Counter till length of data (Message)
    #Traverse the image
    for i in range(c-1):
        for j in range(r-1):
            if ctr<len(x):
                try:
                    arr[i][j][0]=hide(data1[i][j][0],x[ctr]) #Hide message in the pixel
                    ctr+=1
                except:
                    print(i,j) #Exception handling for debiggung
                    break
               


    #print(arr)
    
    image_arr=numpy.array(arr).astype(numpy.uint8)
    #print(image_arr)

    image_arr2=Image.fromarray(image_arr)
    #image_arr2=image_arr2.save('imgdemo.png')
    #image_arr2.show()
    return image_arr2

#--------------------------Decryption-------------------------#


def decode(img):
    if(img.size[0]==256 or img.size[1]==256 or img.size[0]==257 or img.size[1]==257):
        r,c=img.size[0],img.size[1]
        data=asarray(img)
        data1=data.tolist()
        #print(r,c)
        output=''
        y=''
        for i in 'wearempstmemomoteam':
            y+=format(ord(i), '08b')
        n=len(y)
        ctr=0
        flag= 'encrypted'
        
        for i in range(c-1):
            if flag!='encrypted':
                break
            for j in range(r-1):
                if c<n:
                    try:
                        if data1[i][j][0]!= int(y[ctr]) and i!=0 and j!=0:
                            flag='not enc'
                            print(i,j)
                            break
                    except:
                        print(i,j)
                        pass
                        
                elif ctr==n:
                    flag='enc'
                    break
                
                ctr+=1
                

        if(flag=='encrypted' or flag=='enc'):
            #print(output)
            y=''
            for i in '$$$':
                y+=format(ord(i), '08b')
            for i in range(c-1):
                for j in range(r-1):
                    try:
                        if y in output:
                            flag=True
                            break
                        else:
                            output+=unhide(data1[i][j][0])
                    except:
                        print(i,j)
            
            #print(output)

            str_data =' '
            

            for i in range(0, len(output), 8): 
                
            
                temp_data = int(output[i:i + 8]) 
                decimal_data = BinaryToDecimal(temp_data) 
                str_data = str_data + chr(decimal_data)  

            
            return str_data[(len("wearempstmemomoteam")+1):-3].strip()
        else:
            print(flag)
            return "There is no message in the image or the image has been modified [Try a different image]"
    else:
        return "There is no message in the image or the image has been modified"
def decrypt(img):
    return decode(img)
    

    
'''image1 = Image.open('q.png')
x=encode(image1, input())
x.show()
x.convert('RGB').save('new1.png')'''
#img=Image.open('C:/Users/rutvik/Desktop/PFE/new1 (25).png')
#print(decrypt(img))