from django.shortcuts import render
from django.http import HttpResponse
from flarm.models import GfsaFlarmRecords,GfsaFlarmTimeStamp
from flight.models import GfsaFlightRecords,GfsaGliderFlarmFlightRecords,GfsaTugFlarmFlightRecords
from glider.models import GfsaGliders
from tug.models import GfsaTugs
from gfsa.settings import *
import httplib
import time as tm
import datetime
from xml.dom import minidom
#xml tree functions for the xml data
def get_xml():
    return 1
#get the attribute of node
def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

#get the value of node
def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node != [] and node.childNodes[index].nodeValue else ''

#get the xml node
def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

#transfer the xml to string
def xml_to_string(filename='user.xml'):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')

#get the xml from the flarmradar websit
#the url is made my the launcpe 
#offset is the number of page in website.
def get_xml_file(t,launch_type,offset):

    date=str(t[0])+"/"+str(t[1])+"/"+str(t[2])
    filename="record-"+str(t[0])+"-"+str(t[1])+"-"+str(t[2])+launch_type+".xml"

    #connect to the flarm server
    conn = httplib.HTTPConnection(FLARM_DOMAIN)
    conn.request("GET", "/rest/flarmdata/"+launch_type+'/'+FLARM_NODE_NAME+'/'+date+\
                 "?offset="+str(offset))
    r1 = conn.getresponse()
    return r1.read()
    
#build the xml dom
def build_xml_dom(t,launch_type,xml_str):
    filename="record-"+str(t[0])+"-"+str(t[1])+"-"+str(t[2])+launch_type+".xml"
    xml_dom = minidom.parseString(xml_str)
    return xml_dom

#get the data from the website
#@parameter is the date and the lauch type
def get_data(time,launch_type):
    list_=[]
    has_more="true"
    offset=0
    #when has more is true
    #offset +25 for next page 
    while has_more == "true":
        xml_dom=build_xml_dom(time,launch_type,get_xml_file(time,launch_type,offset))
        root = xml_dom.getElementsByTagName("rest"+launch_type.capitalize()+"QueryResult")[0]
        has_more_node=root.getElementsByTagName("hasMore")[0]
        has_more=has_more_node.childNodes[0].data
        #print has_more,launch_type
        if has_more:
          offset+=25
        states = root.getElementsByTagName(launch_type+"s")[0]
        count = 0

        for state in states.getElementsByTagName(launch_type):
          count+=1
          plane = get_xmlnode(state,"plane")[0]
          flarmId_plane = get_nodevalue(get_xmlnode(plane,"flarmId")[0])
          launch_type_plane =get_nodevalue(get_xmlnode(plane,"type")[0])
          time_plane = get_nodevalue(get_xmlnode(state,"time")[0])
          list_+=[(flarmId_plane,(launch_type,time_plane))]
    return list_

#main flarm api 
def flarm_api_all(request):
    oneday=datetime.timedelta(1)
    # year=date.tm_year
    # month=date.tm_mon
    # day=date.tm_mday
    date_stamp=GfsaFlarmTimeStamp.objects.all()
    if len(date_stamp)==0 :
      date_stamp=GfsaFlarmTimeStamp()
      date_stamp.date_stamp=datetime.datetime(2014,8,9)
    else:
      date_stamp=date_stamp[0]
    print date_stamp.date_stamp,'asdasdasdhiausdghiaushd'
    if not TEST_FLARM:
      now=datetime.datetime.today()
    else:
      now=datetime.datetime(2014,8,10)
    while (date_stamp.date_stamp.date() <= now.date()):
      save_flarm_([date_stamp.date_stamp.year,date_stamp.date_stamp.month,date_stamp.date_stamp.day])
      date_stamp.date_stamp+=oneday
    match_flarm()
    response = HttpResponse("successfully save all before"+str(date_stamp.date_stamp.date()))
    date_stamp.save()
    return response



def flarm_api(request):
    if not TEST_FLARM:
      time=[tm.localtime()[0],tm.localtime()[1],tm.localtime()[2]]
    else:
      time=[2014,8,10]#for test
    save_flarm_(time)
    match_flarm()
    response = HttpResponse("successfully save on "+str(time[0])+'-'+str(time[1])+'-'+str(time[2]))
    return response

def save_flarm_(time):
  #get landing data and takeoff data seperately
    list_of_landing = get_data(time,"landing")
    list_of_takeoff = get_data(time,"takeoff")
    list_of_all=list_of_landing+list_of_takeoff

    count_tf=0
    count_ld=0
    #combine the two list together and sort by time:
    for (flarmId_plane,(launch_type,time_plane)) in sorted(list_of_all,lambda x,y:cmp(x[1][1],y[1][1])):
      #fix the datetime format
      year=time_plane[:4]
      month=time_plane[5:7]
      day=time_plane[8:10]
      hour =int(time_plane[11:13])
      minuts= time_plane[14:16]
      seconds=time_plane[17:19]
      t=(int(year),int(month),int(day),int(hour),int(minuts),int(seconds))
      time_plane = datetime.datetime(*t[:6])
      if tm.localtime().tm_isdst==1:
        hour_delta=9
      else:
        hour_delta=8
      hour_ = datetime.timedelta(hours=hour_delta)
      time_plane+=hour_
      #for take off time and handle the exception of time/record lost
      if(launch_type=="takeoff"):
        count_tf+=1
        try:
          flarm_record = GfsaFlarmRecords.objects.get(flmr_id=flarmId_plane,takeoff_time=time_plane)
        except:    
          try:
              flarm_record=GfsaFlarmRecords.objects.get(flmr_id=flarmId_plane,flmr_states="flying")
              flarm_record.flmr_states ="no_landing"
          except:
              flarm_record = GfsaFlarmRecords()
              flarm_record.flmr_id=flarmId_plane
              flarm_record.takeoff_time=time_plane
              flarm_record.flmr_states ="flying"
      #for the landing handle the data lost
      else:
        count_ld+=1
        try:
          flarm_record = GfsaFlarmRecords.objects.get(flmr_id=flarmId_plane,landing_time=time_plane)
        except:
          try:
              flarm_record = GfsaFlarmRecords.objects.get(flmr_id=flarmId_plane,flmr_states="flying")
              flarm_record.landing_time=time_plane
              flarm_record.flmr_states ="landed"
          except:
              flarm_record = GfsaFlarmRecords()
              flarm_record.flmr_id=flarmId_plane
              flarm_record.flmr_states ="no_takeoff" 
              flarm_record.landing_time=time_plane
              #if (count_ld == 1):
                #print "count ld = 1 and save with no take off"
      flarm_record.save()

def match_flarm():
  flight_sheet_all=GfsaFlightRecords.objects.all()
  flarm_record_all=GfsaFlarmRecords.objects.all()
  glider_flarm_rd_all=GfsaGliderFlarmFlightRecords.objects.all()
  tug_flarm_rd_all=GfsaTugFlarmFlightRecords.objects.all()
  for flight_sheet_record in flight_sheet_all:
    fr_id=flight_sheet_record.fr_id
    glider= flight_sheet_record.glider_glider
    tug=flight_sheet_record.tug_tug
    if glider != None:
        glider_flarm_id=flight_sheet_record.glider_glider.glider_flarm_id
        #print 'try to find record with id = ',fr_id
        #print 'glider id = ',glider_flarm_id==None
        if len(glider_flarm_id)!=6:
          continue
        try:  
          GfsaGliderFlarmFlightRecord=GfsaGliderFlarmFlightRecords.objects.get(flight_record_id=flight_sheet_record)
        except:
          GfsaGliderFlarmFlightRecord= GfsaGliderFlarmFlightRecords()
          GfsaGliderFlarmFlightRecord.flight_record_id=flight_sheet_record
          GfsaGliderFlarmFlightRecord.flarm_id=glider.glider_flarm_id
          GfsaGliderFlarmFlightRecord.save()
        GfsaGliderFlarmFlightRecord.take_off,GfsaGliderFlarmFlightRecord.landing= get_closest_flarm(flight_sheet_record,glider_flarm_id)
        GfsaGliderFlarmFlightRecord.save()
    #add tug
    if tug != None:
        tug_flarm_id=flight_sheet_record.tug_tug.tug_flarm_id
        if tug_flarm_id=='':
          continue
        if len(tug_flarm_id)!=6:
          continue
        #print 'tug flarm id =',tug_flarm_id

        try:  
          GfsaTugFlarmFlightRecord=GfsaTugFlarmFlightRecords.objects.get(flight_record_id=flight_sheet_record)
        except:
          GfsaTugFlarmFlightRecord= GfsaTugFlarmFlightRecords()
          GfsaTugFlarmFlightRecord.flight_record_id=flight_sheet_record
          GfsaTugFlarmFlightRecord.flarm_id=tug.tug_flarm_id
          GfsaTugFlarmFlightRecord.save()
        GfsaTugFlarmFlightRecord.take_off,GfsaTugFlarmFlightRecord.landing= get_closest_flarm(flight_sheet_record,tug_flarm_id)
        GfsaTugFlarmFlightRecord.save()

def get_closest_flarm(flight_sheet_record,flarm_id):
    flarm_records=GfsaFlarmRecords.objects.filter(flmr_id=flarm_id)
    if len(flarm_records) == 0:
      return None,None
    #do closest time calculation:
    flarm_records=same_date(flarm_records,flight_sheet_record.fr_take_off)
    closest_record=None


    if len(flarm_records)==0:
      return None,None
    closest_record = flarm_records[0]
    gap = get_gap(closest_record.takeoff_time,flight_sheet_record.fr_take_off)
    closest_time=gap
    count=1
    #print 'closest_time ',count,closest_time
    for flarm_record in flarm_records:
      if flarm_record.takeoff_time == None:
        continue
      #print flarm_record.takeoff_time,flight_sheet_record.fr_take_off,closest_record.takeoff_time
      gap=get_gap(flarm_record.takeoff_time,flight_sheet_record.fr_take_off)
      #print flarm_record.takeoff_time,'gap is',gap
      if gap<closest_time:
        closest_time=gap
        closest_record = flarm_record
      count+=1
    #print flight_sheet_record.fr_take_off,closest_record.takeoff_time
    if closest_record==None:
      return None,None
    return closest_record.takeoff_time,closest_record.landing_time
def get_gap(d1,d2):
    try:
      if (d1>=d2):
        return (d1-d2).seconds
      else:
        return (d2-d1).seconds

    except:
      return 100000000000000000000000#as a large gap

def same_date(records,date):
  answer=[]
  for record in records:
    #print record.takeoff_time.date(),date
    try:
      if record.takeoff_time==None:
        continue
      if(record.takeoff_time.date()==date.date()):
        answer+=[record]
    except:
      continue
  return answer

  


# Create your views here.
