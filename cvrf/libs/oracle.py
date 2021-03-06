from django.conf import settings
from eulexistdb import db

from datetime import date

thisyear = date.today().year

class connExistDB:	  
	def __init__(self):
		self.db = db.ExistDB()	  
	def get_data(self, query):
		result = list()
		qresult = self.db.executeQuery(query)
		hits = self.db.getHits(qresult)
		for i in range(hits):
			result.append(str(self.db.retrieve(qresult, i)))
		return result
	
def get_qryOracleCvrfCveCpe(cve):
	qry = '''xquery version "3.0";
	declare namespace cvrf = "http://www.icasi.org/CVRF/schema/cvrf/1.1";
	declare namespace prod = "http://www.icasi.org/CVRF/schema/prod/1.1";
	declare namespace vuln = "http://www.icasi.org/CVRF/schema/vuln/1.1";
	let $thiscve := "'''+cve+'''"
	for $cpe in doc('/db/cyberxml/apps/cvrf/oracle.com/oraprodid2cpe.xml')//entry
	for $pid in collection('/db/cyberxml/data/cvrf/oracle.com')//node()[vuln:CVE[.=$thiscve]]/vuln:ProductStatuses/vuln:Status[@Type="Known Affected"]/vuln:ProductID[starts-with(.,$cpe/ProductID/text())]
	return $cpe/CPE2.2/text()'''
	return qry


def getCpeFromCve(cve):
	try:
		qrystr=get_qryOracleCvrfCveCpe(cve)
		a = connExistDB()
		cpes =list(set(a.get_data(qrystr)))
		cpes.sort()
	except:
		cpes=[]
	return(cpes)
