import pandas as pd 
import subprocess as sp
import os
import time

####################################################################
wifiname=input("wifiname: ")
wifipass=input("wifipass: ")
h=wifiname.encode('utf-8')
profilename=input("wifi profilename: ")
path=(os.path.dirname(__file__))

"""
######################### Get WIFI interface card ###################
w=sp.Popen("netsh wlan show interface | findstr Name", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
stdout=w.communicate()
d=stdout[0].decode()
wf=d.split("\n")
wf.remove(wf[-1])
print(wf)
################# 
wflist=[]
for i in wf:
    line=i.replace("Name","")
    line=line.replace(":","")
    line=line.replace("\r","")
    line=line.strip()
    wflist.append(line)
print("List wifi of this PC:")
print(wflist)

############################ Get all profile #################################

p=sp.Popen("netsh wlan show profiles | findstr \"All User Profile\"", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
stdout1,stderr1=p.communicate()
pf=stdout1.decode()

for j in wflist:
    pf=pf.replace("Profiles on interface {}:".format(j),"")

pf=pf.replace("User profiles","")
pf=pf.replace("All User Profile     :","")
pf=pf.replace("\r\n","")
pf=pf.replace("    ","")
pf=pf.strip()
pf=pf.split()
pf=list(set(pf))
print("Wifi Profile on System:")
print(pf)
"""
############################### Delete all Wifi profile ###################
print("Delete all Wifi Profile:")

dl=sp.Popen("netsh wlan delete profile name=*", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
stdout2,stderr2=dl.communicate()
print(stdout2)

############################################################################
print("Adding wifi profile:")
############ Create xml wifi-profile ######################################
xml=open("{}.xml".format(profilename),"w")
xml.close()
xml=open("{}.xml".format(profilename),"a")
xml.write('<?xml version="1.0"?>\n')
xml.write('<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">\n')
xml.write('    <name>{}</name>\n'.format(wifiname))
xml.write('    <SSIDConfig>\n')
xml.write('        <SSID>\n')
xml.write('            <hex>{}</hex>\n'.format(h.hex()))
xml.write('            <name>{}</name>\n'.format(wifiname))
xml.write('        </SSID>\n')
xml.write('    </SSIDConfig>\n')
xml.write('    <connectionType>ESS</connectionType>\n')
xml.write('    <connectionMode>auto</connectionMode>\n')
xml.write('    <MSM>\n')
xml.write('        <security>\n')
xml.write('            <authEncryption>\n')
xml.write('                <authentication>WPA2PSK</authentication>\n')
xml.write('                <encryption>AES</encryption>\n')
xml.write('                <useOneX>false</useOneX>\n')
xml.write('            </authEncryption>\n')
xml.write('            <sharedKey>\n')
xml.write('                <keyType>passPhrase</keyType>\n')
xml.write('                <protected>false</protected>\n')
xml.write('                <keyMaterial>{}</keyMaterial>\n'.format(wifipass))
xml.write('            </sharedKey>\n')
xml.write('        </security>\n')
xml.write('    </MSM>\n')
xml.write('    <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">\n')
xml.write('        <enableRandomization>false</enableRandomization>\n')
xml.write('    </MacRandomization>\n')
xml.write('</WLANProfile>')
xml.close()

sp.Popen('netsh wlan add profile filename="{}/{}.xml" user=current'.format(path,profilename),shell=True)
time.sleep(3)
print("finish!")











