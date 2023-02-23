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
        file = new_dir / 'file.tmp'
        write_file(new_dir, 'file.tmp', b'content', dry_run)
        yield {'dir': new_dir, 'file': file}

    @pytest.mark.parametrize('dry_run', [False])
    def test_create_directory(self, write):
        ''' create directory'''
        assert write.get('dir').exists()

    @pytest.mark.parametrize('dry_run', [True])
    def test_dryrun_directory(self, write):
        ''' dry_run blocks directory creation'''
        assert not write.get('dir').exists()

    @pytest.mark.parametrize('dry_run', [False])
    def test_write_file(self, write):
        ''' write file'''
        assert write.get('file').exists()

    @pytest.mark.parametrize('dry_run', [True])
    def test_dryrun_file(self, write):
        ''' - dry_run blocks file creation'''
        assert not write.get('file').exists()

