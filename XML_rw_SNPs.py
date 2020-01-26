import xml.etree.ElementTree as ET
import xml.sax
from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd
from sklearn import svm
#read_xmlfile = ET.parse('C:\\Users\\kiit1\\Documents\\snp_result.xml')
#metadata_root = read_xmlfile.getroot()
#for latest in metadata_root.findall('Rs'):
#       latest_version = latest.find('Ss')
#        print(latest_version)
def encodealleles(allele):
    if allele == 'A':
        return 1
    elif allele == 'T':
        return 2
    elif allele == 'C':
        return 3
    elif allele == 'G':
        return 4
    else:
        return 0

#Step-1
# Open XML document using minidom parser
DOMTree1 = xml.dom.minidom.parse("C:\\Users\\kiit1\\Documents\\dataSnp\\Diabatic_snp_result.xml")
collection1 = DOMTree1.documentElement

DOMTree2 = xml.dom.minidom.parse("C:\\Users\\kiit1\\Documents\\dataSnp\\Chrons_snp_result.xml")
collection2 = DOMTree2.documentElement

DOMTree3 = xml.dom.minidom.parse("C:\\Users\\kiit1\\Documents\\dataSnp\\patient_SNPs.xml")
e = xml.etree.ElementTree.parse('C:\\Users\\kiit1\\Documents\\dataSnp\\patient_SNPs.xml').getroot()
collection3 = DOMTree3.documentElement

#if collection.hasAttribute("shelf"):
#   print "Root element : %s" % collection.getAttribute("shelf")

# Get all the movies in the collection
#step-2
rs = collection1.getElementsByTagName("Rs")
rs2 = collection2.getElementsByTagName("Rs")
#patients Data
rs3 = collection3.getElementsByTagName("Rs")


# Print detail of each RSID.
rsIdList=[]
for rsid in rs:
   if rsid.hasAttribute("rsId"):
      print(rsid.getAttribute("rsId"))
      rsIdList.append(rsid.getAttribute("rsId"))

print(len(rsIdList))

rsIdList2=[]
for rsid2 in rs2:
   if rsid2.hasAttribute("rsId"):
      print(rsid2.getAttribute("rsId"))
      rsIdList2.append(rsid2.getAttribute("rsId"))

print(len(rsIdList2))

rsIdList3=[]
for rsid3 in rs3:
   if rsid3.hasAttribute("rsId"):
      print(rsid3.getAttribute("rsId"))
      rsIdList3.append(rsid3.getAttribute("rsId"))

print(len(rsIdList3))

arrySup=[]
chk_Ch_list = []
for rsId_diabetic in rsIdList:
    i=0
    for rsId_patient in rsIdList3:
        if rsId_diabetic == rsId_patient:
            chk_Ch_list.append(rsId_patient)
            i=i+1
    arrySup.append(i)
print(arrySup)

arryChromosome = []
#step-3
#eclit Algorithm

#total number of SNPs
total_SNPs = len(rsIdList3)
extxtIndex = 0
for i in arrySup:
    support = (i/total_SNPs)*100
    if support > 0.4:#it represent at list one chromosome exits in patient SNPs set
        arryChromosome.append(rsIdList3[extxtIndex])
    extxtIndex = extxtIndex + 1




    print("Support= %s" % support)
print(len(arryChromosome))

#Extract SNPs for test
indexval = 0
fer_array = []
allele_array = []
for chomosome in arryChromosome:
    for atype in e.findall('Rs'):
        try:
            print(chomosome, ' ==', atype.get('rsId'))
            if chomosome == atype.get('rsId'):
                print('-------------------------------------------------------------------')
                print(atype.findall('Frequency')[0].get('freq'))
                fer_array.append(atype.findall('Frequency')[0].get('freq'))
                allele_array.append(encodealleles(atype.findall('Frequency')[0].get('allele')))
            indexval = indexval + 1

        except IndexError:
            print("err........")


print(fer_array)

dataFrame = pd.DataFrame(
    {'frequency': fer_array,
     'allele': allele_array,
    })
print(dataFrame)
#step-4
# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

X_test = sc.fit_transform(dataFrame)

#load SVM model
from sklearn.externals import joblib
clf = joblib.load('C:\\Users\\kiit1\\Documents\\dataSnp\\Diabatic.pkl')

result = clf.predict(dataFrame)
print(result)
#accuracy calculation
i = 0
p = 0
n = 0

while i<len(result):
    if result[i] == 1:
        p = p+1
    else:
        n = n+1
    i = i+1

print("Among ", len(result) ,"SNPs ",p,"numbers are Shown to be diabatic type-2 and ",n ," Are look like negetive")

print(len(e))
#we take 21 negetive SNPs for Diabatic and 237 diabatic SNPs accuracy is calculated as
# (positive_count - 21)/total
acuracy = ((p-21)/len(result))*100
print("acuracy = ", acuracy,"%")

df = pd.read_csv('C:\\Users\\kiit1\\Documents\\dataSnp\\out.csv')
#print(df.iloc[:, 1:3])
pre1 = df.iloc[:, 1:3].values
print(clf.predict(sc.fit_transform(pre1)))
