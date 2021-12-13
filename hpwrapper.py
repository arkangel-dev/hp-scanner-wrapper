import json
import requests
import xml.etree.ElementTree as ET
import webbrowser
from const import *
import urllib.request 


class Wrapper():
	payload="""<scan:ScanSettings xmlns:scan="http://schemas.hp.com/imaging/escl/2011/05/03" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/" xmlns:dd3="http://www.hp.com/schemas/imaging/con/dictionaries/2009/04/06" xmlns:fw="http://www.hp.com/schemas/imaging/con/firewall/2011/01/05" xmlns:scc="http://schemas.hp.com/imaging/escl/2011/05/03" xmlns:pwg="http://www.pwg.org/schemas/2010/12/sm"><pwg:Version>2.1</pwg:Version><scan:Intent>Photo</scan:Intent><pwg:ScanRegions><pwg:ScanRegion><pwg:Height>3507</pwg:Height><pwg:Width>2481</pwg:Width><pwg:XOffset>0</pwg:XOffset><pwg:YOffset>0</pwg:YOffset></pwg:ScanRegion></pwg:ScanRegions><pwg:InputSource>Platen</pwg:InputSource><scan:DocumentFormatExt>image/jpeg</scan:DocumentFormatExt><scan:XResolution>300</scan:XResolution><scan:YResolution>300</scan:YResolution><scan:ColorMode>RGB24</scan:ColorMode><scan:CompressionFactor>25</scan:CompressionFactor><scan:Brightness>1000</scan:Brightness><scan:Contrast>1000</scan:Contrast></scan:ScanSettings>"""
	rootIp = ""

	def __init__(self, _rip):
		self.rootIp = _rip


	def ScanDocument(self, outputfile):
		requests.post(self.rootIp + '/eSCL/ScanJobs', data=self.payload, headers=headers, verify=False)
		for job in self.GetJobs():
			if not job.State in {"Aborted", "Completed"}:  
				urllib.request.urlretrieve(job.GetLink(), outputfile)

	def GetJobs(self):
		raw = requests.get(self.rootIp + "/eSCL/ScannerStatus", headers=headers, verify=False)
		status = ET.fromstring(raw.content)
		jobs_raw = list(status.find("scan:Jobs", ns))
		parsed_job_list = []
		for job in jobs_raw:
			cj = ScanJob(self.rootIp)
			cj.ParseJob(job)
			parsed_job_list.append(cj)
		return parsed_job_list
		
class ScanJob:
	RootDomain = ""
	URI = ""
	UUID = ""
	Age = ""
	State = ""
	StateReasons = []
	ImagesCompleted = 0
	ImagesToTransfer = 0

	def __init__(self, rd):
		self.StateReasons = []
		self.RootDomain = rd
	
	def ParseJob(self, val):
		self.State = val.find("pwg:JobState", ns).text
		self.URI = val.find("pwg:JobUri", ns).text
		self.UUID = val.find("pwg:JobUuid", ns).text
		self.Age = val.find("scan:Age", ns).text
		self.ImagesCompleted = val.find("pwg:ImagesCompleted", ns).text
		self.ImagesToTransfer = val.find("pwg:ImagesToTransfer", ns).text
		for x in list(val.find("pwg:JobStateReasons",ns)):
			self.StateReasons.append(x.text)
		
	def GetLink(self):
		return self.RootDomain + self.URI + "/NextDocument"
	