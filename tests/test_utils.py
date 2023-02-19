import pytest
import yaml
from utils import cleanse_filename, write_file


TESTDATA = 'tests/testdata.yaml'


class TestCleanseFilename():
    def get_data(cls: str, test: str, file=TESTDATA):
        with open(file, 'r') as fl:
            dict = yaml.load(fl, Loader=yaml.FullLoader)
        list = dict.get(cls).get(test)
        return {'ids': [i.get('id') for i in list],
                'test': [(k, v) for item in list
                         for k, v in item.get('test').items()]}

    cls, test = ('CleanseFilename', 'test_cleanse_filename')
    data = get_data(cls, test)
    @pytest.mark.parametrize('_in,_out', data.get('test'), ids=data.get('ids'))
    def test_cleanse(self, _in, _out):
        assert cleanse_filename(_in) == _out


class TestWriteFile():
    @pytest.fixture
    def write(self, tmp_path, dry_run):
        new_dir = tmp_path / 'new_dir'
        write_file(new_dir, 'file.tmp', b'content', dry_run)
        yield new_dir

    @pytest.mark.parametrize('dry_run', [False])
    def test_create_directory(self, write):
        ''' - create directory'''
        assert write.exists()

    # def test_write_file():
    #     ''' - write file'''
    #     pass

    # def test_dryrun_directory():
    #     ''' - dry_run blocks directory creation'''
    #     pass

    # def test_dryrun_file():
    #     ''' - dry_run blocks file creation'''
    #     pass
