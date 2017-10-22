
#coding=utf-8



import cgi
import cx_Oracle
import time


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
curdate=time.strftime('%Y/%m/%d',time.localtime(time.time()))
curtime=time.strftime('%H',time.localtime(time.time()))
#curdatetime=time.strftime('%Y/%m/%d/%H:%M',time.localtime(time.time()))
# Get data from fields
location = form.getvalue('location')
if (location == None):
	location=1

selectggsn=form.getvalue('selectggsnname')
if(selectggsn==None):
	selectggsn='all'
startdate = form.getvalue('selectstartdate')
if (startdate == None):
	startdate=curdate
stopdate = form.getvalue('selectstopdate')
if (stopdate == None):
	stopdate=curdate
starttime = form.getvalue('selectstarttime')
if (starttime == None ):
	starttime="00"
stoptime = form.getvalue('selectstoptime')
if (stoptime == None):
	stoptime=curtime

selectalarm = form.getvalue('selectalarm')
if (selectalarm == None or selectalarm==''):
	selectalarm='all'
	
startdatetime=startdate+"/"+starttime+":00"
stopdatetime=stopdate+"/"+stoptime+":00"
#print curtime
db = cx_Oracle.connect('kiu', 'antkiu123', '10.221.213.28:1521/OSS')
cursor=db.cursor()


# ALARM
sqlstring="""
select objects.INT_ID ,
objects.name,
DN,alarm_number,alarm_time,cancel_time,alarm_status,
alarm_type,severity,
text,
fx_alarm.SUPPLEMENTARY_INFO
from fx_alarm,objects
where 
NE_ID=objects.int_id and (objects.object_class=3529) 
"""

if (selectggsn!='all'):
	sqlstringggsn=" and objects.name=\'"+selectggsn+"\' " 
else:
	sqlstringggsn=" "
	
if (selectalarm!='all'):
	sqlstringalarm=" and alarm_number=\'"+selectalarm+"\' "
else:
	sqlstringalarm=" "
	
sqlstringtime=" and to_char(fx_alarm.alarm_time,\'yyyy/mm/dd/hh24:mi\')<\'"+stopdatetime+"\' and to_char(fx_alarm.alarm_time,\'yyyy/mm/dd/hh24:mi\')>\'"+startdatetime+"\' "

sqlstringorder="""
order by objects.int_id , alarm_type desc ,severity asc
"""

sqlstring=sqlstring+sqlstringggsn+sqlstringalarm+sqlstringtime+sqlstringorder 
#print sqlstring

cursor.execute(sqlstring)

row=cursor.fetchall()


print 'Status: 200 OK'
print 'Content-type: text/xml charset=GB2312;\n'


print "<?xml version=\"1.0\" encoding=\"GB2312\"?>"
print "<response>"
print "<location>"
print "<locationid>1</locationid>"
print "<passed>true</passed>"
print "<message>�����澯</message>"
print "<Title>"
print "<name>�豸ID</name>"
print "<name>�豸����</name>"
print "<name>���ϵ�Ԫ</name>"
print "<name>�澯��</name>"
print "<name>�澯����ʱ��</name>"
print "<name>�澯ȡ��ʱ��</name>"
print "<name>�澯״̬</name>"
print "<name>�澯����</name>"
print "<name>�澯����</name>"
print "<name>�澯����</name>"
print "<name>�澯������Ϣ</name>"
print "</Title>"

for x in row:
	print "<Item>"
	for y in x:
		print "<ItemCol>"
		print "<value>"
		print y
		print "</value>"
		print "</ItemCol>"
	print "</Item>"

print "</location>"



print "</response>"
