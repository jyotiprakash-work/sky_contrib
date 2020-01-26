from xml.dom.minidom import parse
import xml.dom.minidom
from sklearn import svm
import pandas as pd
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
DOMTree1 = xml.dom.minidom.parse("C:\\Users\\kiit1\\Documents\\dataSnp\\Chrons_snp_result.xml")
collection1 = DOMTree1.documentElement

rs = collection1.getElementsByTagName("Rs")


# Print detail of each RSID.
rsIdList=[]
Observed_allels = []
for rsid in rs:

   if rsid.hasAttribute("rsId"):
      #print(rsid.getAttribute("rsId"))
      rsIdList.append(rsid.getAttribute("rsId"))
   '''Frequency = rsid.getElementsByTagName("Frequency")
   for feq in Frequency:
       if feq.hasAttribute("freq"):
           print(rsid.getAttribute("freq"))
       if feq.hasAttribute("allele"):
           print(rsid.getAttribute("allele"))
'''

fer_array = []
allele_array = []
import xml.etree.ElementTree
e = xml.etree.ElementTree.parse('C:\\Users\\kiit1\\Documents\\dataSnp\\Diabatic_snp_result.xml').getroot()
ef = xml.etree.ElementTree.parse('C:\\Users\\kiit1\\Documents\\dataSnp\\Chrons_snp_result.xml').getroot()

try:

    for atype in e.findall('Rs'):
        try:
            print('-------------------------------------------------------------------')
            print(atype.findall('Frequency')[0].get('freq'))
            fer_array.append(atype.findall('Frequency')[0].get('freq'))
            allele_array.append(encodealleles(atype.findall('Frequency')[0].get('allele')))
        except IndexError:
            print("err........")

finally:
    print('Not found')
print(len(rsIdList))
print(allele_array)
print(fer_array)

#negetive data
f_fer_array = []
f_allele_array = []
try:

    for ftype in ef.findall('Rs'):
        #print('-------------------------------------------------------------------')
        try:
            print(ftype.findall('Frequency')[0].get('freq'))
            f_fer_array.append(ftype.findall('Frequency')[0].get('freq'))
            f_allele_array.append(encodealleles(ftype.findall('Frequency')[0].get('allele')))
        except IndexError:
            print('IndexError')



finally:
    print('Not found')
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print(len(f_allele_array))

lebel = []
for i in range(229):
    lebel.append(1)
for i in range(13):
    lebel.append(0)

dataFrame = pd.DataFrame(
    {'frequency': fer_array+ f_fer_array,
     'allele': allele_array+f_allele_array,
     'lebel': lebel
    })
print(dataFrame)
dataFrame.to_csv('out1.csv')
clf = svm.SVC(kernel='rbf', gamma=0.001, C=100)
trainedSet = dataFrame.iloc[40:240, 0:2]
trainedSetLebel = dataFrame.iloc[40:240, 2]
print(trainedSet)
print(trainedSetLebel)
# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

clf.fit(sc.fit_transform(trainedSet),trainedSetLebel)
testSet = pd.concat([dataFrame.iloc[0:40, 0:2], dataFrame.iloc[235:241, 0:2]])
testSet.to_csv('out.csv')
print('----------------------------------------------------------')
print(testSet)
print('----------------------------------------------------------')
result = clf.predict(sc.fit_transform(testSet))
print(sc.fit_transform(testSet))
print(result)
accuracy = clf.score(sc.fit_transform(testSet), result)
print(accuracy)

#realResult = pd.concat(dataFrame.iloc[0:40, 2] , dataFrame.iloc[235:241, 2])
realResult1 = dataFrame.iloc[0:40, 2]
realResult2 = dataFrame.iloc[235:241, 2]
realResult = pd.concat([realResult1, realResult2])

print(len(result))
print(len(realResult.values))
realResult = realResult.values

#accuracy calculation
i = 0
p = 0
n = 0

while i<len(result):
    if result[i] == realResult[i]:
        p = p+1
    else:
        n = n+1
    i = i+1
print(p)
print(n)

increse = ((len(realResult) - n)/len(realResult))*100
decrese = ((len(realResult) - p)/len(realResult))*100
print("increse % =", increse)
print("decrese % =", decrese)

#saveing SVM model into a plk file
from sklearn.externals import joblib
joblib.dump(clf, 'C:\\Users\\kiit1\\Documents\\dataSnp\\Diabatic.pkl')
#print(dataFrame.iloc[11:12])