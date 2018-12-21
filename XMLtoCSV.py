import xml.etree.ElementTree as ET
import csv
import os
import urllib2
from datetime import datetime

def loadXML(xmlurl):
    url = xmlurl
    reply = urllib2.urlopen(url)
    resp = reply.read()
    with open('Booj.xml', 'wb') as f:
        f.write(resp)

def parseXML(xmlfile, tempFile):

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    open_write = open(tempFile, 'w')
    csv_write = csv.writer(open_write)

    listingHead = []

    count = 0
    for node in root.findall('Listing'):
        listings = []
        bathrooms = []
        appliances = []
        roomlist = []

        if count == 0:

            mlsid = None
            mlsname = None

            for details in node.findall('ListingDetails'):
                date = details.find('DateListed').tag
                listingHead.append(date)
                price = details.find('Price').tag
                listingHead.append(price)
                mlsid = details.find('MlsId').tag
                mlsname = details.find('MlsName').tag
                break
            for details in node.findall('Location'):
                address = details.find('StreetAddress').tag
                listingHead.append(address)
                break
            for details in node.findall('BasicDetails'):
                bed = details.find('Bedrooms').tag
                listingHead.append(bed)
                bath = details.find('Bathrooms').tag
                listingHead.append(bath)
                desc = details.find('Description').tag
                listingHead.append(desc)
                listingHead.append(mlsid)
                listingHead.append(mlsname)
            for details in node.findall('RichDetails'):
                try:
                    apps = details.find('Appliances').tag
                    listingHead.append(apps)
                except:
                    listingHead.append('Appliances').tag
                try:
                    rooms = details.find('Rooms').tag
                    listingHead.append(rooms)
                except:
                    listingHead.append('Rooms')

                count = count + 1

        #boolean so we only add 2016 years and AND descriptions
        add = None

        mlsid = None
        mlsname = None

        for details in node.findall('ListingDetails'):
            date = details.find('DateListed').text
            if date[:4] == '2016':
                listings.append(date[:10])
                add = True
            price = details.find('Price').text
            listings.append(price)
            mlsid = details.find('MlsId').text
            mlsname = details.find('MlsName').text
        for details in node.findall('Location'):
            lo = details.find('StreetAddress').text
            listings.append(lo)
        for details in node.findall('BasicDetails'):
            bed = details.find('Bedrooms').text
            listings.append(bed)
            fullbath = details.find('FullBathrooms').text
            if fullbath is not None:
                bathrooms.append('Full Bathrooms ' + fullbath)
            halfbath = details.find('HalfBathrooms').text
            if halfbath is not None:
                bathrooms.append(' Half Bathrooms ' + halfbath)
            quarterbath = details.find('ThreeQuarterBathrooms').text
            if quarterbath is not None:
                bathrooms.append(' Three Quarter Bathrooms ' + quarterbath)
            listings.append(bathrooms)
            desc = details.find("Description").text
            listings.append(desc[:200])
            listings.append(mlsid)
            listings.append(mlsname)
            if 'and' not in desc[:200]:
                add = False
        for details in node.findall('RichDetails'):
            try:
                for apps in details.iter('Appliances'):
                    for app in apps.iter('Appliance'):
                        appliance = app.text
                        appliances.append(appliance)
            except:
                appliance = None
            try:
                for room in details.iter('Rooms'):
                    for roo in room.iter('Room'):
                        rooms = roo.text
                        roomlist.append(rooms)
            except:
                rooms = None

            listings.append(appliances)
            listings.append(roomlist)

        if add:
            csv_write.writerow(listings)
            # instead of writing out bathrooms can add them to say 2.5 bath

    return listingHead

def sort(tempFile, fileLo, listingHead):

    readTmp = csv.reader(open(tempFile, 'r'))

    readTmp = sorted(readTmp, key = lambda row: datetime.strptime(row[0], "%Y-%m-%d"))

    open_write = open(fileLo, 'w')
    csv_write = csv.writer(open_write)

    with open(fileLo, 'w') as f:
        csv_write.writerow(listingHead)

        for row in readTmp:
            csv_write.writerow(row)

    if os.path.exists(tempFile):
       os.remove(tempFile)
    else:
        print('file does not exist')

def main():
    url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    load = loadXML(url)

    tempFile = '/tmp/BoojCodeTemp.csv'
    listingHead = parseXML('Booj.xml', tempFile)

    finalFile = '/tmp/BoojCode.csv'
    sort(tempFile, finalFile, listingHead)

if __name__ == "__main__":

    main()

