BUTTON_TEST_RESULTS = (
    ('/test/results?testsite=controlplans', 'Controplans'),
    ('/test/results?testsite=elspot', 'Elspot'),
)

TEST_DATES = (
    '2022-10-30', # 25 hour date
    '2022-12-01', # a quite normal one
    '2023-03-26', # 23 hour date
    '2023-04-10', # includes negative prices
)

# only these regions will have plots generated during test-run
GENERATED_PLOT_REGIONS = (
    'Oslo',
    'Tr.heim',
    'DK1',
    'SE1',
)

BUTTON_TEST_RESULTS_CONTROLPLAN_PLAN_NAME = (
    ('/test/results?testsite=controlplans&plan_name=example_time_schedule', 'example_time_schedule'),
    ('/test/results?testsite=controlplans&plan_name=example_elspot_schedule', 'example_elspot_schedule'),
    ('/test/results?testsite=controlplans&plan_name=test_uploaded_controlplan', 'test_uploaded_controlplan'),
)

BUTTON_TEST_RESULTS_ELSPOT_REGION = (
    ('/test/results?testsite=elspot&region=Bergen', 'Bergen'),
    ('/test/results?testsite=elspot&region=DK1', 'DK1'),
    ('/test/results?testsite=elspot&region=DK2', 'DK2'),
    ('/test/results?testsite=elspot&region=EE', 'EE'),
    ('/test/results?testsite=elspot&region=FI', 'FI'),
    ('/test/results?testsite=elspot&region=Kr.sand', 'Kr.sand'),
    ('/test/results?testsite=elspot&region=LT', 'LT'),
    ('/test/results?testsite=elspot&region=LV', 'LV'),
    ('/test/results?testsite=elspot&region=Molde', 'Molde'),
    ('/test/results?testsite=elspot&region=Oslo', 'Oslo'),
    ('/test/results?testsite=elspot&region=SE1', 'SE1'),
    ('/test/results?testsite=elspot&region=SE2', 'SE2'),
    ('/test/results?testsite=elspot&region=SE3', 'SE3'),
    ('/test/results?testsite=elspot&region=SE4', 'SE4'),
    ('/test/results?testsite=elspot&region=SYS', 'SYS'),
    ('/test/results?testsite=elspot&region=Tr.heim', 'Tr.heim'),
    ('/test/results?testsite=elspot&region=Troms%C3%B8', 'Tromsø'),
)
