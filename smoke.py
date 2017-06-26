# bailii-feed-parser.py
# (c) 2017. Daniel Hoadley
# This program parses a BAILII RSS feed, extracts information from it and writes a docket
# for each case in the feed.

import feedparser
import re
from xml.etree.ElementTree import Element, SubElement
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    # Return a pretty-printed XML string for the Element.

    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Parse the feed
d = feedparser.parse('######')
count = 0

# Loop over the entries in the feed
for entry in d.entries:

    # Extract the contents of all <item><title> tags
    case_entry = entry.title
    # Extract the date of judgment
    date = re.findall(r'\d\d\s\w+\s\d\d\d\d', case_entry)
    # Extract the neutral citation
    ncit = re.findall(r'\[\d\d\d\d\]\s\w+\s\d+\s\W\w+\W', case_entry)
    # Extract the case name
    case_name_fetch = re.findall(r'^.*\s\[', case_entry)
    # Remove opening [ from case name match
    case_name = [s.strip(' [') for s in case_name_fetch]
    count = count+1
    # Get the URL for the case on BAILII
    BAILIILink = entry.link

    #Stringify components

    case_name_clean = ''.join(case_name)
    date_clean = ''.join(date)
    ncit_clean = ''.join(ncit)

    # Parse the date for re-use in the docket filename and in the DOJ field

    converter = time.strptime(date_clean, '%d %b %Y')
    converted_date = time.strftime('%Y-%m-%d', converter)

    # Set the court

    court = 'QBD'

    # Open each link in the feed and pull the case number out of the HTML

    req = Request(BAILIILink, headers={'User-Agent': 'Mozilla/5.0'})
    open_page = urlopen(req).read()
    soup = BeautifulSoup(open_page, 'lxml')
    case_number_tag = soup.find('casenum')
    case_number_text = case_number_tag.text
    # Clean the casenumber of unwanted leading characters
    case_number = case_number_text[9:]

    # Create output docket filename

    file_date = time.strftime('%Y%m%d', converter)
    case_name_nospace = case_name_clean.replace(' ', '_')
    output_name = file_date + '[DK]' + case_name_nospace + '.xml'
    print (output_name)

    # Build docket for each case in the feed

    docket = Element ('Docket')
    CaseInfoElement = SubElement(docket, 'CaseInfo')
    TeamContextElement = SubElement(CaseInfoElement, 'TeamContext')
    ReporterElement = SubElement(CaseInfoElement, 'ReporterName')
    DoJElement = SubElement(CaseInfoElement, 'DoJ')
    DoJElement.text = converted_date
    CaseNumberElement = SubElement(CaseInfoElement, 'CourtFileNo')
    CaseNumberElement.text = case_number
    CourtAbbrevElement = SubElement(CaseInfoElement, 'CourtAbbrev')
    CourtAbbrevElement.text = court
    AllNCitElement = SubElement(CaseInfoElement, 'AllNCit')
    NCitElement = SubElement(AllNCitElement, 'NCit')
    NCitElement.text = ncit_clean
    CaseMainElement = SubElement(CaseInfoElement, 'CaseMain')
    IxCardNoElement = SubElement(CaseMainElement, 'IxCardNo')
    TempIxCardNoElement = SubElement(CaseMainElement, 'TempIxCardNo')
    FullReportNameElement = SubElement(CaseMainElement, 'FullReportName')
    FullReportNameElement.text = case_name_clean
    AltNameElement = SubElement(CaseMainElement, 'AltName')
    CaseJointElement = SubElement(CaseInfoElement, 'CaseJoint')
    JointCaseIxCardNoElement = SubElement(CaseJointElement, 'IxCardNo')
    JointCaseTempIxCardNoElement = SubElement(CaseJointElement, 'TempIxCardNo')
    JointCaseReportNameElement = SubElement(CaseJointElement, 'FullReportName')
    JointCaseReportCaseNameElement = SubElement(CaseJointElement, 'CaseName')
    BenchElement = SubElement(CaseInfoElement, 'Bench')
    JudgeElement = SubElement(BenchElement, 'Judge')
    LegalTopicsElement = SubElement(CaseInfoElement, 'LegalTopics')
    LegalTopic1Element = SubElement(LegalTopicsElement, 'LegalTopic1')
    ReportabilityElement = SubElement(CaseInfoElement, 'Reportability')
    ReportingDecisionElement = SubElement(ReportabilityElement, 'ReportingDecision')
    ReportabilitNotesElement = SubElement(ReportabilityElement, 'ReportabilityNotes')
    EditorialNotesElement = SubElement(docket, 'EditorialNotes')
    ReporterNotesElement = SubElement(EditorialNotesElement, 'ReporterNotes')
    TeamLeaderNotesElement = SubElement(EditorialNotesElement, 'TeamLeaderNotes')
    ProductionNotesElement = SubElement(EditorialNotesElement, 'ProductionNotes')
    TypesetterInfoElement = SubElement(docket, 'TypesetterInfo')
    TypesetterNotesElement = SubElement(TypesetterInfoElement, 'TypesetterNotes')
    RunningHeaderElement = SubElement(TypesetterInfoElement, 'RunningHeader')
    CoverMaterialElement = SubElement(TypesetterInfoElement, 'CoverMaterial')
    CatchWordElement = SubElement(CoverMaterialElement, 'CatchWord')
    CatchWordElement = SubElement(CoverMaterialElement, 'CatchWord')
    CatchWordElement = SubElement(CoverMaterialElement, 'CatchWord')
    SubjectInfoElement = SubElement(docket, 'SubjectInfo')
    SubjectMatterElement = SubElement(SubjectInfoElement, 'SubjectMatter')
    SubjectMatterWLRDElement = SubElement(SubjectMatterElement, 'SubjectMatterWLRD')
    CatchWordElement = SubElement(SubjectMatterWLRDElement, 'Catchword', attrib={'pos':'1'})
    CatchWordElement = SubElement(SubjectMatterWLRDElement, 'Catchword', attrib={'pos': '2'})
    CatchWordElement = SubElement(SubjectMatterWLRDElement, 'Catchword', attrib={'pos': '3'})
    SubjectMatterChElement = SubElement(SubjectMatterElement, 'SubjectMatterCh')
    SubjectMatterFamElement = SubElement(SubjectMatterElement, 'SubjectMatterFam')
    SubjectMatterACElement = SubElement(SubjectMatterElement, 'SubjectMatterAC')
    SubjectMatterQBElement = SubElement(SubjectMatterElement, 'SubjectMatterQB')
    SubjectMatterICRElement = SubElement(SubjectMatterElement, 'SubjectMatterICR')
    SubjectMatterBusLRElement = SubElement(SubjectMatterElement, 'SubjectMatterBuslr')
    SubjectMatterPTSRElement = SubElement(SubjectMatterElement, 'SubjectMatterPTSR')
    WordsPhraseElement = SubElement(SubjectInfoElement, 'WordsPhrases')
    IxEntryWPElement = SubElement(WordsPhraseElement, 'IxEntryWP')
    ShipsNamesElement = SubElement(SubjectInfoElement, 'ShipsNames')
    IxEntrySNElement = SubElement(ShipsNamesElement, 'IxEntrySN')
    CasesJudConElement = SubElement(docket, 'CasesJudCon')
    IxEntryCJCon = SubElement(CasesJudConElement, 'IxEntryCJCon')
    IxCardNoCJCon = SubElement(IxEntryCJCon, 'IxCardNo')
    CJConCaseNameElement = SubElement(IxEntryCJCon, 'CaseName')
    CJConNCitElement = SubElement(IxEntryCJCon, 'NCit')
    IxRefsCJConElement = SubElement(IxEntryCJCon, 'IxRefs')
    ConsiderElement = SubElement(IxEntryCJCon, 'Consider', attrib={'conType':'approved'})
    LegislationElement = SubElement(docket, 'Legislation')
    PublishingInfoElement = SubElement(docket, 'PublishingInfo')
    ICLRseriesPubrefsElement = SubElement(PublishingInfoElement, 'ICLRseriesPubrefs')
    ExtPubrefsElement = SubElement(PublishingInfoElement, 'ExtPubrefs')
    TranscriptFileElement = SubElement(PublishingInfoElement, 'TranscriptFile')
    BAILIILinkElement = SubElement(PublishingInfoElement, 'BailiiLink')
    BAILIILinkElement.text = BAILIILink
    LifecycleStatusElement = SubElement(PublishingInfoElement, 'LifecycleStatus')

    # Write the docket to a new file

    f = open(output_name, 'w')
    f.write(prettify(docket))
    f.close()

    # Prettify

    print(prettify(docket))





