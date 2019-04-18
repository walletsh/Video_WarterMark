
import rarfile
import os

inPath  = '/Users/imwallet/Downloads/codepay.rar'
outPath = '/Users/imwallet/Downloads/'

# rf = rarfile.RarFile(inPath)
# rf.extractall(outPath)



def un_rar(file_name):
    """unrar zip file"""
    rar = rarfile.RarFile(file_name)
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    os.chdir(file_name + "_files")
    retval = os.getcwd()
    print('retval: {}'.format(retval))
    rar.extractall(file_name + "_files")
    rar.close()

if __name__ == '__main__':

    un_rar(inPath)