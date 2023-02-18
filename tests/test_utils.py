import pytest
from utils import cleanse_filename


TESTDATA = 'tests/testdata.yaml'


def parse_yaml(file='metadata.yaml') -> dict:
    with open(file, 'r') as fl:
        dict = yaml.load(fl, Loader=yaml.FullLoader)
    return dict


TESTDATA = {'a:k_a-a)a(a a': 'a:k_a_a_a_a_a'}
td = [(_in, _out) for _in, _out in TESTDATA.items()]

@pytest.mark.parametrize("_in,_out", td)
def test_cleanse_filename(_in, _out):
    assert cleanse_filename(_in) == _out

# class TestCleanseFilename():

#     @pytest.fixture
#     def testdata(self,  l):
#         # td = parse_yaml(TESTDATA).get('CleanseFilename').get('test_cleanse_filename')
#         td = TESTDATA
#         return [(_in, _out) for _in, _out in td.items()]

#     @pytest.mark.parametrize("_in,_out", testdata)
#     def test_clease_filename(self, _in, _out):
#         '''
#         Test cases
#         - special characters replaced with _
#         - repeated special characters reduced to a single _
#         - leading and trailing _ removed
#         - returns lowcase
#         '''
#         assert cleanse_filename(_in) == _out
