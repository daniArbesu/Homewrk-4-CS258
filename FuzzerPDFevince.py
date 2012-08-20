import random
import math
import string
import subprocess
import time
import os

#Fuzzer "babysitting an army of monkeys"

#list of files for seed:
file_list=[
"we_media_espanol.pdf",
"Guia_MusicaCineTelevision_Internet.pdf",
"1.pdf",
"fw4.pdf",
"hayalternativas.pdf",
"mabi.pdf"]

#aplicaciones:
apps = [
"evince"
]

FuzzFactor = 10
num_tests = 10000
fuzz_output = "fuzz.pdf"


for i in range(num_tests):
    
    file_choice = random.choice(file_list)
    app=random.choice(apps)
    buf = bytearray(open("./PDF/"+file_choice, 'rb').read())

    # start Charlie Miller code
    if i % 50 == 0:     #variamos el factor de fuzzing
        FuzzFactor+=10
    numwrites=random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)
    # end Charlie Miller code

    open(fuzz_output, 'wb').write(buf)
    
    process = subprocess.Popen([app, fuzz_output])
    #stdout=process.stderr.read()
    
    time.sleep(1)
    
    if process.poll():
        # programa crash
        # copiamos el pdf causante a una carpeta aparte
        print "Crashed"
        #print stdout
        os.system("cp "+fuzz_output+" ./crashed_pdf/"+str(time.time())+".pdf")
        print "Return code: "+ str(process.returncode) + " \n"
    else:
        #process.terminate()
        try:
            process.terminate()
        except OSError:
            print "Forced to terminate"

