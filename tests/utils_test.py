import pytest


class CleanseFilename:
    '''
    Test cases
    - special characters replaced with _
    - repeated special characters reduced to a single _
    - leading and trailing _ removed 
    - returns lowcase
    '''


    @pytest.mark.parametrize("in,out", 
    def test_clease_filename():
        assert cleanse_filename(filename) == answer
