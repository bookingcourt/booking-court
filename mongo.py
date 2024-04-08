from datetime import date, timedelta
from mongoengine import *
import datetime
import json


isConnected = False

class District(Document):
    area_id = LongField(required=True)
    area_code = StringField(required=True, max_length=10)
    area_enName = StringField(required=True, max_length=1000)
    area_tcName = StringField(required=True, max_length=1000)
    area_scName = StringField(required=True, max_length=1000)
    dist_id = LongField(required=True)
    dist_code = StringField(required=True, max_length=10)
    dist_enName = StringField(required=True, max_length=1000)
    dist_tcName = StringField(required=True, max_length=1000)
    dist_scName = StringField(required=True, max_length=1000)
    create_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField()

class Session(EmbeddedDocument):
    fa_code = StringField(required=True, max_length=10)
    ssn_code = StringField(required=True, max_length=50)
    ssn_StartDate = DateField(required=True)
    ssn_StartTime = StringField(required=True, max_length=10)
    ssn_EndTime = StringField(required=True, max_length=10)
    available = BooleanField()
    peak = BooleanField()
    ssn_cnt = IntField()
    create_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField()    

class Venue(Document):
    dist_code = StringField(required=True, max_length=10)
    venue_id = LongField(required=True)
    venue_imageUrl = StringField(max_length=1000)
    venue_enName = StringField(max_length=1000)
    venue_tcName = StringField(max_length=1000)
    venue_scName = StringField(max_length=1000)
    venue_enAddr = StringField(max_length=1000)
    venue_tcAddr = StringField(max_length=1000)
    venue_scAddr = StringField(max_length=1000)
    venue_phone = StringField(max_length=100)
    venue_lat = StringField(max_length=100)
    venue_long = StringField(max_length=100)
    venue_wkdayHr = StringField(max_length=100)
    venue_wkendHr = StringField(max_length=100)
    create_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField()
    fa_codes = ListField(StringField(max_length=50))
    sessions = ListField(EmbeddedDocumentField(Session))    

class Facility(Document):
    fa_id = LongField(required=True)
    fa_code = StringField(required=True, max_length=10)
    fa_groupCode = StringField(required=True, max_length=10)
    fa_enName = StringField(max_length=1000)
    fa_tcName = StringField(max_length=1000)
    fa_scName = StringField(max_length=1000)
    create_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField()

class DataInfo(Document):
    info_type = StringField(required=True, max_length=20)
    day = StringField(max_length=2)
    modified_date = DateTimeField()

def checkIsConnected():
    global isConnected
    return isConnected

def connectDB():
    global isConnected
    # connect to mongodb atlas
    url = 'mongodb+srv://tester01:XwhvEmdR4vOfoZo6@cluster0.6amlp.gcp.mongodb.net/sportcenter?retryWrites=true&w=majority'
    # connect to local mongodb server    
    # url = 'mongodb+srv://testing:QwITuYfge9hOW8am@cluster0-6amlp.gcp.mongodb.net/myDB?retryWrites=true&w=majority'    
    # connect to local mongodb server
    # url = 'mongodb://testing:QwITuYfge9hOW8am@192.168.188.97:27017/myDB?retryWrites=true&w=majority&authSource=users'
    connect(host=url)
    isConnected = True

    # db = get_db()

def disconnectDB():
    disconnect()
    isConnected = False

def insertOrUpdateDataInfo(info_type, day = None):
    if checkIsConnected() == False:
        connectDB()
    try:
        info = DataInfo.objects(info_type=info_type,day=day).first()
        if info == None:
            info = DataInfo()
            info['info_type'] = info_type
            if day != None:
                info['day'] = day
        info['modified_date'] = datetime.datetime.now
        info.save()
        return True
    except Exception as error:
        print(error)
        return False

def getDataInfoDT(info_type):
    if checkIsConnected() == False:
        connectDB()
    try:    
        info = DataInfo.objects(info_type=info_type).first()
        if info != None:
            return info['modified_date']
        return None
    except Exception as error:
        print(error)
        return None


# def removeOldDataInfo(info_type):
#     if checkIsConnected() == False:
#         connectDB()
#     try:
#         today = datetime.datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
#         find_query = {'modified_date': {'$lt':today}, 'info_type': info_type}
#         cnt = DataInfo.objects(__raw__=find_query).delete()        
#         return cnt
#     except Exception as error:
#         print('error: ', error)
#         return False      

def updateDBFields(docu, obj, fields):
    for field in fields:
        if field in obj and obj[field] != None:
            docu[field] = obj[field]
    docu['modified_date'] = datetime.datetime.now

def getDistByArea(area_code):
    if checkIsConnected() == False:
        connectDB()
    return District.objects(area_code=area_code)    

def updateDistrict(oDist):
    if checkIsConnected() == False:
        connectDB()
    try:
        dist = District.objects(dist_id=oDist['dist_id'], dist_code=oDist['dist_code']).first()
        if dist == None: 
            return False
        updateDBFields(dist, oDist, ['area_code', 'area_enName', 'area_tcName', 'area_scName', 'dist_enName', 'dist_tcName', 'dist_scName'])
        dist.save()
        return True
    except:
        return False

def saveDistrict(oDist):
    if checkIsConnected() == False:
        connectDB()
    dist = District()
    updateDBFields(dist, oDist, ['area_id', 'area_code', 'area_enName', 'area_tcName', 'area_scName', 
                                'dist_id', 'dist_code', 'dist_enName', 'dist_tcName', 'dist_scName'])
    dist.save()
    return True


def findVenue(oVenue):
    if checkIsConnected() == False:
        connectDB()
    try:
        return Venue.objects(venue_id=oVenue['venue_id']).first()        
    except:
        return None

def updateVenue(oVenue, info = False):
    if checkIsConnected() == False:
        connectDB()
    try:
        venue = findVenue(oVenue)
        if venue == None: 
            return False        
        if info == True:
            updateDBFields(venue, oVenue, ['venue_enAddr', 'venue_tcAddr', 'venue_scAddr', 'venue_phone', 'venue_lat', 'venue_long', 'venue_wkdayHr', 'venue_wkendHr'])       
        else:
            if not (oVenue["fa_code"] in venue["fa_codes"]):
                venue["fa_codes"].append(oVenue["fa_code"])

            updateDBFields(venue, oVenue, ['dist_code', 'venue_imageUrl', 'venue_enName', 'venue_tcName', 'venue_scName'])
        venue.save()
        return True
    except:
        return False    

def saveVenue(oVenue):
    if checkIsConnected() == False:
        connectDB()
    venue = Venue()
    venue["fa_codes"].append(oVenue["fa_code"])
    updateDBFields(venue, oVenue, ['dist_code', 'venue_id', 'venue_imageUrl', 'venue_enName', 'venue_tcName', 'venue_scName'])
    venue.save()

def updateFa(oFa):
    if checkIsConnected() == False:
        db = connectDB()
    try:
        fa = Facility.objects(fa_id=oFa['fa_id']).first()
        if fa == None: 
            return False
        updateDBFields(fa, oFa, ['fa_code', 'fa_groupCode','fa_enName', 'fa_tcName', 'fa_scName'])
        fa.save()
        return True
    except:
        return False     

def saveFa(oFa):
    if checkIsConnected() == False:
        connectDB()
    fa = Facility()
    updateDBFields(fa, oFa, ['fa_id', 'fa_code', 'fa_groupCode', 'fa_enName', 'fa_tcName', 'fa_scName'])
    fa.save()

def createSsn(oSsn):
    if checkIsConnected() == False:
        connectDB()
    ssn = Session()
    updateDBFields(ssn, oSsn, ['fa_code', 'ssn_code', 'ssn_StartDate', 'ssn_StartTime', 'ssn_EndTime', 'available', 'peak', 'ssn_cnt'])
    return ssn

def saveSsnToVenue(venue, ssn):    
    if venue == None:
        return False
    venue.sessions.append(ssn)
    venue.save()
    return True

def updateSsn(oSsn):
    if checkIsConnected() == False:
        connectDB()
    try:        
        cnt = Venue.objects(venue_id=oSsn['venue_id'], sessions__ssn_code=oSsn['ssn_code']) \
                    .update(\
                        set__sessions__S__ssn_cnt=oSsn['ssn_cnt'],
                        set__sessions__S__modified_date=datetime.datetime.now \
                    )
        return cnt
        # Find ssn_code and return ssn (embeddeddocument)
        # ssn = list(Venue.objects.aggregate(
        #     {"$unwind": "$sessions" },
        #     {"$match":{"venue_id":209, "sessions.ssn_code":"BASC_20231114090000"} },            
        #     {"$group":{"_id": None, "list":{"$push":"$sessions"}}}
        # ))
        # print(ssn)
    except:
        return 0    

def removeOldSsn(typeCode):
    if checkIsConnected() == False:
        connectDB()
    try:
        today = datetime.datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
        find_query = {'sessions.ssn_StartDate': {'$lt':today}}
        update_query = {'$pull': {'sessions' : {'ssn_StartDate': {'$lt':today}}}}
        # cnt = Venue.objects(__raw__=find_query).delete()
        cnt = Venue.objects(__raw__=find_query).update(__raw__=update_query)    
        return cnt
    except Exception as error:
        print('error: ', error)
        return False


# records = Record.objects()

# i = 0
# for crt in records:
#     # name = crt.centreName.replace(' - Arena','')
#     name = crt.centreName
#     charEnd = name.rfind(' -')
#     if charEnd == -1:
#         charEnd = name.rfind(' (')
#     if charEnd > -1:
#         name = name[0:charEnd]
    
#     info = CourtInfo.objects(venueDisplay=name).first()
#     if info == None:
#         print (i, name)
#     # else:
#         # print (i, name, info.pk)

#         # print (info.venueDisplay)
#     i = i + 1
    
# disconnectDB()




# if checkIsConnected() == False:
#     connectDB()

# saveCourtInfo(cData)

# # saveToDB(gData)

# if checkIsConnected():
#     disconnectDB()

# connectDB()
# records = Record.objects(uid__lte = "20190907")
# for rec in records:
#     rec.delete()
#     print (rec.uid)
# disconnectDB()



# print (db.name)

# class Post(Document):
#     title = StringField(required=True, max_length=200)
#     content = StringField(required=True)
#     author = StringField(required=True, max_length=50)
#     published = DateTimeField(default=datetime.datetime.now)

# post_1 = Post(
#     title='Sample Post',
#     content='Some engaging content',
#     author='Scott'
# )
# post_1.save()       # This will perform an insert
# print(post_1.title)
# post_1.title = 'A Better Post Title'
# post_1.save()       # This will perform an atomic edit on "title"
# print(post_1.title)


    
# ts = Timeslot(time='7am-13pm', status='OK')
# crt = Court(uid=1, name = 'My Court')

# crt.timeslots.append(ts)

# rec = Record(uid='20190910')

# updated = Record.objects(courts__uid=crt.uid).update_one(set__courts__S=crt)
# if not updated:
#     rec.courts.append(crt)

# rec.save()

# timeslot = Timeslot(time='7-13', status='OK')

# updated = Record.objects(uid=123).update_one(set__remark='hello world222')
# updated = Record.objects(courts__uid=1).update_one(set__courts__S__name='HK Court')
# updated = Record.objects(courts__uid=1).update_one(set__courts__S__timeslots__S=timeslot)

# rec = Record.objects(uid='20190910').first()
# rec.courts[0].name = 'Your court'
# rec.courts.append(crt)
# rec.save()


# print (Record.objects.first().courts[0].name)






