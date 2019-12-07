import pytest
from Algorithm import AlgorithmClass as aC
from Algorithm import algorithm1 as al1


@pytest.fixture
def rfa():
    rfa = aC.Algorithm("RelativeFrequencyAlgorithm", al1.csv_lib_creator,
                       al1.csv_reader, 'csv', 'csv', 'RFA')
    return rfa



@pytest.mark.AlgorithmClass
def test_algorithm_creation(rfa):
    assert rfa.name == "RelativeFrequencyAlgorithm"
    assert callable(rfa.request_function) is True
    assert callable(rfa.training_function) is True
    assert rfa.file_types == dict(crawler='csv', library='csv')
    assert rfa.trained is False
    assert rfa.library_filename == 'Library_RFA.csv'
    assert rfa.teams == set()

    rfa.train('TestData(2018).csv')
    assert rfa.trained is True


def test_name_as_libname():
    rfa2 = aC.Algorithm("RelativeFrequencyAlgorithm", al1.csv_lib_creator,
                        al1.csv_reader, 'csv', 'csv')
    assert rfa2.library_filename == 'Library_RelativeFrequencyAlgorithm.csv'


def test_algorithm_class_result_dict():
    host = 'Munich'
    results = [0, 0.2, 0.8]
    assert aC.results_to_dict(host, results) == dict(host='Munich', win=0, lose=0.2, draw=0.8)


def test_algorithm1_result_dict_error1():
    host = 'Munich'
    results = [0, 0, 0]  # not normalized
    results2 = [0, 'hello', 1]  # not numbers only
    results3 = [-1, 1, 1]  # not normalized
    with pytest.raises(ValueError):
        aC.results_to_dict(host, results)
        aC.results_to_dict(host, results2)
        aC.results_to_dict(host, results3)


# Checks whether the wrong file types are detected
def test_algorithm_class_train_error1(rfa):
    with pytest.raises(ValueError):
        rfa.train('TestData(2018).xls')  # ends with xls


# Checks whether a library is created
def test_algorithm_class_train_creation(rfa):
    with open('TestData(2018).csv') as data:
        rfa.train('TestData(2018).csv')
        next(data)  # skips the header.
        with open('Library_RFA.csv') as Library:
            assert Library.read() == data.read()
        Library.close()
    data.close()

    assert rfa.trained is True
    assert rfa.teams != set()  # checks if the


# Checks whether requesting without training raises an Error
def test_algorithm_class_request_error1(rfa):
    with pytest.raises(NameError):
        rfa.request(dict(host='FC Bayern', guest='1899 Hoffenheim'))


# Checks whether not listed team names are detected
def test_algorithm_class_request_error1(rfa):
    rfa.train('TestData(2018).csv')
    with pytest.raises(ValueError):
        rfa.request(dict(host='FC Bayern', guest='Bad Input'))
        rfa.request(dict(host='Bad Input', guest='FC Bayern'))


# Checks whether the outcome is correct for an example
def test_algorithm_class_request(rfa):
    rfa.train('TestData(2018).csv')
    assert rfa.request(dict(host='FC Bayern', guest='Werder Bremen')) ==\
           dict(host='FC Bayern', win=1, lose=0, draw=0)


# Just visualisation. Uncomment below to see
def algorithm1_print_running():
    rfa = aC.Algorithm("RelativeFrequencyAlgorithm", al1.csv_lib_creator,
                       al1.csv_reader, 'csv', 'csv')

    rfa.train('TestData(2018).csv')

    def print_results(host, guest):
        print('Statistic for ' + host + ' against ' + guest + ':')
        results = rfa.request(dict(host=host, guest=guest))
        for (x, y) in results.items():
            print(x + ": " + str(y))
        print()

    print_results('Borussia Dortmund', 'SC Freiburg')
    print_results('SC Freiburg', 'FC Bayern')

# Uncomment this to see some output
algorithm1_print_running()
