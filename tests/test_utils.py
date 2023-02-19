import pytest
import yaml
from utils import cleanse_filename


TESTDATA = 'tests/testdata.yaml'


def data(cls: str, test: str, file=TESTDATA):
    with open(file, 'r') as fl:
        dict = yaml.load(fl, Loader=yaml.FullLoader)
    list = dict.get(cls).get(test)
    return {'ids': [i.get('id') for i in list],
            'test': [(k, v) for item in list
                     for k, v in item.get('test').items()]}


cls, test = ('CleanseFilename', 'test_cleanse_filename')
@pytest.mark.parametrize('_in,_out', data(cls, test).get('test'),
                         ids = data(cls, test).get('ids'))
def test_cleanse_filename(_in, _out):
    assert cleanse_filename(_in) == _out
