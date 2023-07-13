"""Test module for table_extractor.py"""

import os
import pytest
from services.extraction.table_extractor import TableExtractor

JSON_FILE_PATH = os.path.join("testing", "pla_extraction_sample.json")

#pylint: disable= protected-access,pointless-string-statement

@pytest.fixture(name="get_table_extractor_object")
def fixture_get_table_extractor_object():
  json_path = JSON_FILE_PATH
  table_extractor_object = TableExtractor(json_path)
  return table_extractor_object


def test_course_extract(get_table_extractor_object):
  expected_output = [
    {
      "keys": ["Credits", "Course", "Credits"],
      "values": [["0.50", "0.50", "0.50", "0.50", "0.50", "0.25", "0.50", None,
      "9.75"], ["13120 American Literature (Honors)", "43410 Geometry",
      "23610 United States History (Honors)", "33110 Environmental Science",
      "53820- Spanish", "91510 Art", "99210 Health", "Semester GPA",
      "Cumulative GPA"], ["0.50", "0.50", "0.50", "0.50", "0.50", "0.50",
      "0.50", None, "13.25"]], "confidence": [[0.99976027, 0.99978155,
      0.99980056, 0.99973786, 0.99973571, 0.99980539, 0.99960518, None,
      0.99941039], [0.99988645, 0.99990773, 0.99992675, 0.99986404, 0.9998619,
      0.99993157, 0.99973142, 0.99401915, 0.99953663], [0.99985754, 0.99987876,
      0.99989784, 0.99983513, 0.99983299, 0.99990261, 0.99970245, None,
      0.99950767]]
    }]
  final_tables_list = [
    {
      "table_id": 0, "header_data": [(None, None), (None, None),
      ("Second Semester", 0.99911475), (None, None), (None, None)],
      "row_data": [[("Grade", 0.99977964), ("Credits", 0.9996227),
      ("Course", 0.99974889), ("Grade", 0.99908197), ("Credits", 0.99971998)],
      [("B", 0.99991721), ("0.50", 0.99976027),
      ("13120 American Literature (Honors)", 0.99988645), ("B", 0.99921954),
      ("0.50", 0.99985754)], [("B", 0.99993849), ("0.50", 0.99978155),
      ("43410 Geometry", 0.99990773), ("A", 0.99924082), ("0.50", 0.99987876)],
      [("B", 0.9999575), ("0.50", 0.99980056),
      ("23610 United States History (Honors)", 0.99992675), ("B", 0.99925983),
      ("0.50", 0.99989784)], [("B", 0.9998948), ("0.50", 0.99973786),
      ("33110 Environmental Science", 0.99986404), ("B", 0.99919713),
      ("0.50", 0.99983513)], [("A", 0.99989265), ("0.50", 0.99973571),
      ("53820- Spanish", 0.9998619), ("A", 0.99919498), ("0.50", 0.99983299)],
      [("A", 0.99996233), ("0.25", 0.99980539), ("91510 Art", 0.99993157),
      ("A", 0.99926466), ("0.50", 0.99990261)], [("B", 0.99976218),
      ("0.50", 0.99960518), ("99210 Health", 0.99973142), ("A", 0.99906445),
      ("0.50", 0.99970245)], [(None, None), (None, None),
      ("Semester GPA", 0.99401915), (None, None), (None, None)],
      [("2.90", 0.99956739), ("9.75", 0.99941039),
      ("Cumulative GPA", 0.99953663), ("3.15", 0.99886966),
      ("13.25", 0.99950767)]]}]
  table_entities = {
    "header_list": ["Courses", "Curriculum", "Program", "Syllabus", "Semester",
    "Subject", "Credits"],
    "req_entities": ["Course", "Course_code", "Credit", "Course_Description"]
    }
  output = get_table_extractor_object.course_extract(final_tables_list,
                                                    table_entities)
  assert output == expected_output


def test_filter_table(get_table_extractor_object):
  get_table_extractor_object.table_list = [
    {
      "table_id": 0, "header_data": [(None, None), (None, None),
      ("Second Semester", 0.99911475), (None, None), (None, None)],
      "row_data": [[("Grade", 0.99977964), ("Credits", 0.9996227),
      ("Course", 0.99974889), ("Grade", 0.99908197), ("Credits", 0.99971998)],
      [("B", 0.99991721), ("0.50", 0.99976027),
      ("13120 American Literature (Honors)", 0.99988645), ("B", 0.99921954),
      ("0.50", 0.99985754)], [("B", 0.99993849), ("0.50", 0.99978155),
      ("43410 Geometry", 0.99990773), ("A", 0.99924082), ("0.50", 0.99987876)],
      [("B", 0.9999575), ("0.50", 0.99980056),
      ("23610 United States History (Honors)", 0.99992675), ("B", 0.99925983),
      ("0.50", 0.99989784)], [("B", 0.9998948), ("0.50", 0.99973786),
      ("33110 Environmental Science", 0.99986404), ("B", 0.99919713),
      ("0.50", 0.99983513)], [("A", 0.99989265), ("0.50", 0.99973571),
      ("53820- Spanish", 0.9998619), ("A", 0.99919498), ("0.50", 0.99983299)],
      [("A", 0.99996233), ("0.25", 0.99980539), ("91510 Art", 0.99993157),
      ("A", 0.99926466), ("0.50", 0.99990261)], [("B", 0.99976218),
      ("0.50", 0.99960518), ("99210 Health", 0.99973142), ("A", 0.99906445),
      ("0.50", 0.99970245)], [(None, None), (None, None),
      ("Semester GPA", 0.99401915), (None, None), (None, None)],
      [("2.90", 0.99956739), ("9.75", 0.99941039),
      ("Cumulative GPA", 0.99953663), ("3.15", 0.99886966),
      ("13.25", 0.99950767)]]
    }, {
      "table_id": 1, "header_data": [("Cumulative Weighted GPA", 0.99917698),
      ("3.15/4.00", 0.9999274)], "row_data": [[("Cumulative Unweighted GPA",
      0.99643523), ("3.08/4.00", 0.99718559)], [("HS Units Earned", 0.99911726),
      ("13.25", 0.99986762)], [("Class Rank", 0.99919558),
      ("3/10", 0.99994594)]]}, {"table_id": 2,
      "header_data": [("Date Graduated:", 0.99918914),
      ("Jun 15, 2018", 0.99977517)], "row_data": [[("Guardian:", 0.99919188),
      ("Julie Smith", 0.99977791)], [("Address:", 0.99800843),
      ("123 Maple St", 0.99859446)], [(None, None),
      ("Rockford, IL", 0.99941766)]]}, {"table_id": 3,
      "header_data": [("Name:", 0.99922562), ("John Smith", 0.99856275)],
      "row_data": [[("RPS ID:", 0.99926192), ("12345", 0.99859905)],
      [("Birthdate:", 0.99915004), ("Apr 12, 2001", 0.99848723)],
      [("Gender:", 0.99924606), ("Male", 0.9985832)]]}, {"table_id": 4,
      "header_data": [("is required for a diploma", 0.99959856),
      ("GradeS-Modified", 0.99756551), ("Reg", 0.98694217),
      ("Honors", 0.99892336), ("Advanced/Telescopic", 0.99903232)],
      "row_data": [[(None, None), ("A2", 0.99452806), (None, None),
      ("5", 0.99588591), ("6", 0.99599487)], [("Attendance", 0.99959832),
      ("B2", 0.99756527), ("3", 0.98694193), ("4", 0.99892312),
      ("5", 0.99903208)], [("Fall 2013: 89/95 Spring 2014: 92/95", 0.99904788),
      ("C1", 0.99701482), ("2", 0.98639148), ("3", 0.99837267),
      ("4", 0.99848163)], [("Spring", 0.9990232), ("D1", 0.9969902),
      ("1", 0.98636687), (None, None), (None, None)], [(None, None),
      ("F0", 0.99707633), ("0", 0.986453), (None, None), (None, None)]]}]
  expected_output = [
    {
      "table_id": 0, "header_data": [(None, None), (None, None),
      ("Second Semester", 0.99911475), (None, None), (None, None)],
      "row_data": [[("Grade", 0.99977964), ("Credits", 0.9996227),
      ("Course", 0.99974889), ("Grade", 0.99908197), ("Credits", 0.99971998)],
      [("B", 0.99991721), ("0.50", 0.99976027),
      ("13120 American Literature (Honors)", 0.99988645), ("B", 0.99921954),
      ("0.50", 0.99985754)], [("B", 0.99993849), ("0.50", 0.99978155),
      ("43410 Geometry", 0.99990773), ("A", 0.99924082), ("0.50", 0.99987876)],
      [("B", 0.9999575), ("0.50", 0.99980056),
      ("23610 United States History (Honors)", 0.99992675), ("B", 0.99925983),
      ("0.50", 0.99989784)], [("B", 0.9998948), ("0.50", 0.99973786),
      ("33110 Environmental Science", 0.99986404), ("B", 0.99919713),
      ("0.50", 0.99983513)], [("A", 0.99989265), ("0.50", 0.99973571),
      ("53820- Spanish", 0.9998619), ("A", 0.99919498), ("0.50", 0.99983299)],
      [("A", 0.99996233), ("0.25", 0.99980539), ("91510 Art", 0.99993157),
      ("A", 0.99926466), ("0.50", 0.99990261)], [("B", 0.99976218),
      ("0.50", 0.99960518), ("99210 Health", 0.99973142), ("A", 0.99906445),
      ("0.50", 0.99970245)], [(None, None), (None, None),
      ("Semester GPA", 0.99401915), (None, None), (None, None)],
      [("2.90", 0.99956739), ("9.75", 0.99941039),
      ("Cumulative GPA", 0.99953663), ("3.15", 0.99886966),
      ("13.25", 0.99950767)]]
    }]
  table_entities = {
    "header_list": ["Courses", "Curriculum", "Program", "Syllabus", "Semester",
    "Subject", "Credits"],
    "req_entities": ["Course", "Course_code", "Credit", "Course_Description"]
    }
  output = get_table_extractor_object.filter_table(table_entities)
  assert output == expected_output


def test_table_attributes(get_table_extractor_object):
  expected_master_dict = {
    0: {0: {"headers": [(None, None), (None, None), ("Second Semester",
    0.99911475), (None, None), (None, None)], "page_num": 0,
    0: {"rows": {0: {"value": "Grade", "extraction_confidence": 0.99977964},
    1: {"value": "Credits", "extraction_confidence": 0.9996227},
    2: {"value": "Course", "extraction_confidence": 0.99974889},
    3: {"value": "Grade", "extraction_confidence": 0.99908197},
    4: {"value": "Credits", "extraction_confidence": 0.99971998}}},
    1: {"rows": {0: {"value": "B", "extraction_confidence": 0.99991721},
    1: {"value": "0.50", "extraction_confidence": 0.99976027},
    2: {"value": "13120 American Literature (Honors)",
    "extraction_confidence": 0.99988645},
    3: {"value": "B", "extraction_confidence": 0.99921954},
    4: {"value": "0.50", "extraction_confidence": 0.99985754}}},
    2: {"rows": {0: {"value": "B", "extraction_confidence": 0.99993849},
    1: {"value": "0.50", "extraction_confidence": 0.99978155},
    2: {"value": "43410 Geometry", "extraction_confidence": 0.99990773},
    3: {"value": "A", "extraction_confidence": 0.99924082},
    4: {"value": "0.50", "extraction_confidence": 0.99987876}}},
    3: {"rows": {0: {"value": "B", "extraction_confidence": 0.9999575},
    1: {"value": "0.50", "extraction_confidence": 0.99980056},
    2: {"value": "23610 United States History (Honors)",
    "extraction_confidence": 0.99992675},
    3: {"value": "B", "extraction_confidence": 0.99925983},
    4: {"value": "0.50", "extraction_confidence": 0.99989784}}},
    4: {"rows": {0: {"value": "B", "extraction_confidence": 0.9998948},
    1: {"value": "0.50", "extraction_confidence": 0.99973786},
    2: {"value": "33110 Environmental Science",
    "extraction_confidence": 0.99986404}, 3: {"value": "B",
    "extraction_confidence": 0.99919713}, 4: {"value": "0.50",
    "extraction_confidence": 0.99983513}}}, 5: {"rows": {0: {"value": "A",
    "extraction_confidence": 0.99989265}, 1: {"value": "0.50",
    "extraction_confidence": 0.99973571}, 2: {"value": "53820- Spanish",
    "extraction_confidence": 0.9998619}, 3: {"value": "A",
    "extraction_confidence": 0.99919498}, 4: {"value": "0.50",
    "extraction_confidence": 0.99983299}}}, 6: {"rows": {0: {"value": "A",
    "extraction_confidence": 0.99996233}, 1: {"value": "0.25",
    "extraction_confidence": 0.99980539}, 2: {"value": "91510 Art",
    "extraction_confidence": 0.99993157}, 3: {"value": "A",
    "extraction_confidence": 0.99926466}, 4: {"value": "0.50",
    "extraction_confidence": 0.99990261}}}, 7: {"rows": {0: {"value": "B",
    "extraction_confidence": 0.99976218}, 1: {"value": "0.50",
    "extraction_confidence": 0.99960518}, 2: {"value": "99210 Health",
    "extraction_confidence": 0.99973142}, 3: {"value": "A",
    "extraction_confidence": 0.99906445}, 4: {"value": "0.50",
    "extraction_confidence": 0.99970245}}}, 8: {"rows": {0: {"value": None,
    "extraction_confidence": None}, 1: {"value": None,
    "extraction_confidence": None}, 2: {"value": "Semester GPA",
    "extraction_confidence": 0.99401915}, 3: {"value": None,
    "extraction_confidence": None}, 4: {"value": None,
    "extraction_confidence": None}}}, 9: {"rows": {0: {"value": "2.90",
    "extraction_confidence": 0.99956739}, 1: {"value": "9.75",
    "extraction_confidence": 0.99941039}, 2: {"value": "Cumulative GPA",
    "extraction_confidence": 0.99953663}, 3: {"value": "3.15",
    "extraction_confidence": 0.99886966}, 4: {"value": "13.25",
    "extraction_confidence": 0.99950767}}}}, 1: {"headers": [
    ("Cumulative Weighted GPA", 0.99917698), ("3.15/4.00", 0.9999274)],
    "page_num": 0, 0: {"rows": {0: {"value": "Cumulative Unweighted GPA",
    "extraction_confidence": 0.99643523}, 1: {"value": "3.08/4.00",
    "extraction_confidence": 0.99718559}}}, 1: {"rows": {0: {"value":
    "HS Units Earned", "extraction_confidence": 0.99911726}, 1: {
    "value": "13.25", "extraction_confidence": 0.99986762}}}, 2: {"rows": {0:
    {"value": "Class Rank", "extraction_confidence": 0.99919558}, 1: {"value":
    "3/10", "extraction_confidence": 0.99994594}}}}, 2: {"headers": [
    ("Date Graduated:", 0.99918914), ("Jun 15, 2018", 0.99977517)],
    "page_num": 0, 0: {"rows": {0: {"value": "Guardian:",
    "extraction_confidence": 0.99919188}, 1: {"value": "Julie Smith",
    "extraction_confidence": 0.99977791}}}, 1: {"rows": {0: {"value":
    "Address:", "extraction_confidence": 0.99800843}, 1: {"value":
    "123 Maple St", "extraction_confidence": 0.99859446}}}, 2: {"rows": {0:
    {"value": None, "extraction_confidence": None}, 1: {"value": "Rockford, IL",
    "extraction_confidence": 0.99941766}}}}, 3: {"headers": [
    ("Name:", 0.99922562), ("John Smith", 0.99856275)], "page_num": 0, 0: {
    "rows": {0: {"value": "RPS ID:", "extraction_confidence": 0.99926192}, 1: {
    "value": "12345", "extraction_confidence": 0.99859905}}}, 1: {"rows": {0:
    {"value": "Birthdate:", "extraction_confidence": 0.99915004}, 1: {"value":
    "Apr 12, 2001", "extraction_confidence": 0.99848723}}}, 2: {"rows": {0: {
    "value": "Gender:", "extraction_confidence": 0.99924606}, 1: {"value":
    "Male", "extraction_confidence": 0.9985832}}}}, 4: {"headers": [
    ("is required for a diploma", 0.99959856), ("GradeS-Modified", 0.99756551),
    ("Reg", 0.98694217), ("Honors", 0.99892336), ("Advanced/Telescopic",
    0.99903232)], "page_num": 0, 0: {"rows": {0: {"value": None,
    "extraction_confidence": None}, 1: {"value": "A2", "extraction_confidence":
    0.99452806}, 2: {"value": None, "extraction_confidence": None}, 3: {"value":
    "5", "extraction_confidence": 0.99588591}, 4: {"value": "6",
    "extraction_confidence": 0.99599487}}}, 1: {"rows": {0: {"value":
    "Attendance", "extraction_confidence": 0.99959832}, 1: {"value": "B2",
    "extraction_confidence": 0.99756527}, 2: {"value": "3",
    "extraction_confidence": 0.98694193}, 3: {"value": "4",
    "extraction_confidence": 0.99892312}, 4: {"value": "5",
    "extraction_confidence": 0.99903208}}}, 2: {"rows": {0: {"value":
    "Fall 2013: 89/95 Spring 2014: 92/95", "extraction_confidence":
    0.99904788}, 1: {"value": "C1", "extraction_confidence": 0.99701482}, 2: {
    "value": "2", "extraction_confidence": 0.98639148}, 3: {"value": "3",
    "extraction_confidence": 0.99837267}, 4: {"value": "4",
    "extraction_confidence": 0.99848163}}}, 3: {"rows": {0: {"value":
    "Spring", "extraction_confidence": 0.9990232}, 1: {"value": "D1",
    "extraction_confidence": 0.9969902}, 2: {"value": "1",
    "extraction_confidence": 0.98636687}, 3: {"value": None,
    "extraction_confidence": None}, 4: {"value": None, "extraction_confidence":
    None}}}, 4: {"rows": {0: {"value": None, "extraction_confidence": None},
    1: {"value": "F0", "extraction_confidence": 0.99707633}, 2: {"value": "0",
    "extraction_confidence": 0.986453}, 3: {"value": None,
    "extraction_confidence": None}, 4: {"value": None,
    "extraction_confidence": None}}}}}}
  expected_table_list = [{"table_id": 0, "header_data": [(None, None),
    (None, None), ("Second Semester", 0.99911475), (None, None), (None, None)],
    "row_data": [[("Grade", 0.99977964), ("Credits", 0.9996227),
    ("Course", 0.99974889), ("Grade", 0.99908197), ("Credits", 0.99971998)], [
    ("B", 0.99991721), ("0.50", 0.99976027),
    ("13120 American Literature (Honors)", 0.99988645), ("B", 0.99921954),
    ("0.50", 0.99985754)], [("B", 0.99993849), ("0.50", 0.99978155),
    ("43410 Geometry", 0.99990773), ("A", 0.99924082), ("0.50", 0.99987876)],
    [("B", 0.9999575), ("0.50", 0.99980056),
    ("23610 United States History (Honors)", 0.99992675), ("B", 0.99925983),
    ("0.50", 0.99989784)], [("B", 0.9998948), ("0.50", 0.99973786),
    ("33110 Environmental Science", 0.99986404), ("B", 0.99919713),
    ("0.50", 0.99983513)], [("A", 0.99989265), ("0.50", 0.99973571),
    ("53820- Spanish", 0.9998619), ("A", 0.99919498), ("0.50", 0.99983299)],
    [("A", 0.99996233), ("0.25", 0.99980539), ("91510 Art", 0.99993157), ("A",
    0.99926466), ("0.50", 0.99990261)], [("B", 0.99976218), ("0.50",
    0.99960518), ("99210 Health", 0.99973142), ("A", 0.99906445), ("0.50",
    0.99970245)], [(None, None), (None, None), ("Semester GPA", 0.99401915),
    (None, None), (None, None)], [("2.90", 0.99956739), ("9.75", 0.99941039),
    ("Cumulative GPA", 0.99953663), ("3.15", 0.99886966), ("13.25",
    0.99950767)]]}, {"table_id": 1, "header_data": [("Cumulative Weighted GPA",
    0.99917698), ("3.15/4.00", 0.9999274)], "row_data": [[(
    "Cumulative Unweighted GPA", 0.99643523), ("3.08/4.00", 0.99718559)], [
    ("HS Units Earned", 0.99911726), ("13.25", 0.99986762)], [("Class Rank",
    0.99919558), ("3/10", 0.99994594)]]}, {"table_id": 2, "header_data": [
    ("Date Graduated:", 0.99918914), ("Jun 15, 2018", 0.99977517)],
    "row_data": [[("Guardian:", 0.99919188), ("Julie Smith", 0.99977791)], [
    ("Address:", 0.99800843), ("123 Maple St", 0.99859446)], [(None, None),
    ("Rockford, IL", 0.99941766)]]}, {"table_id": 3, "header_data": [("Name:",
    0.99922562), ("John Smith", 0.99856275)], "row_data": [[("RPS ID:",
    0.99926192), ("12345", 0.99859905)], [("Birthdate:", 0.99915004), (
    "Apr 12, 2001", 0.99848723)], [("Gender:", 0.99924606),
    ("Male", 0.9985832)]]}, {"table_id": 4, "header_data": [
    ("is required for a diploma", 0.99959856), ("GradeS-Modified", 0.99756551),
    ("Reg", 0.98694217), ("Honors", 0.99892336), ("Advanced/Telescopic",
    0.99903232)], "row_data": [[(None, None), ("A2", 0.99452806), (None, None),
    ("5", 0.99588591), ("6", 0.99599487)], [("Attendance", 0.99959832), ("B2",
    0.99756527), ("3", 0.98694193), ("4", 0.99892312), ("5", 0.99903208)], [
    ("Fall 2013: 89/95 Spring 2014: 92/95", 0.99904788), ("C1", 0.99701482),
    ("2", 0.98639148), ("3", 0.99837267), ("4", 0.99848163)], [("Spring",
    0.9990232), ("D1", 0.9969902), ("1", 0.98636687), (None, None), (None,
    None)], [(None, None), ("F0", 0.99707633), ("0", 0.986453), (None, None),
    (None, None)]]}]

  get_table_extractor_object.table_attributes()

  assert get_table_extractor_object.master_dict == expected_master_dict
  assert get_table_extractor_object.table_list == expected_table_list
