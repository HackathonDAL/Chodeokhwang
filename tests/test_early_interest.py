import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import create_app
from backend.scoring import recommend, load_data, load_representative_courses

BASE=['COSE211','COSE212','COSE213','COSE214','COSE222','COSE215','STAT221','STAT232','MATH221']
def sample(codes,interest=3):
    return [dict(course_code=c,grade=4,interest=interest) for c in codes]

class EarlyInterestTests(unittest.TestCase):
    def test_hci_high_interest_with_five_to_ten_courses(self):
        for count in range(5,11):
            with self.subTest(count=count):
                r=recommend(sample(BASE[:count-1])+sample(['COSE432'],5))
                hci=next(f for f in r['top_fields'] if f['field']=='HCI')
                self.assertTrue(hci['early_candidate'])
                self.assertEqual(hci['direct_course_count'],1)
    def test_neutral_single_course_not_promoted(self):
        r=recommend(sample(['COSE432'],3))
        self.assertNotIn('HCI',[f['field'] for f in r['top_fields']])
    def test_indirect_interest_not_promoted(self):
        r=recommend(sample(['MATH221','STAT221','STAT232','COSE281','COSE283'],5))
        for field in ['ML','Computer_Vision','Robotics']:
            f=next(f for f in r['fields'] if f['field']==field)
            self.assertEqual(f['direct_course_count'],0)
            self.assertNotIn(field,[x['field'] for x in r['top_fields']])
    def test_api_explains_early_interest(self):
        with patch.dict('os.environ',{'ENABLE_LLM':'false'}),TestClient(create_app()) as client:
            courses=sample(BASE[:5])+sample(['COSE432'],5)
            r=client.post('/api/analyze',json={'courses':[dict(course_code=c['course_code'],grade='A',interest_score=c['interest']) for c in courses]})
            self.assertEqual(r.status_code,200)
            hci=next(f for f in r.json()['top_fields'] if f['field_id']=='HCI')
            self.assertIn('초기 관심 후보',hci['ai_reason'])
            self.assertEqual(hci['evidence_courses'][0]['course_code'],'COSE432')
    def test_representative_integrity(self):
        courses,matrix=load_data()
        self.assertEqual(len(load_representative_courses(courses,matrix)),16)
