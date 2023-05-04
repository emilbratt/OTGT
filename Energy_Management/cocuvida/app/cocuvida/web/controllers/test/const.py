BUTTON_TEST_SITE_HOME = [
    ['/test?testsite=controlplans', 'Controplans'],
    ['/test?testsite=elspot', 'Elspot'],
]

TEST_DATES = [
    '2022-10-30', # 25 hour date
    '2022-12-01', # a quite normal one
    '2023-03-26', # 23 hour date
    '2023-04-10', # includes negative prices
]

# only these regions will have plots generated during test-run
GENERATED_PLOT_REGIONS = [
    'Oslo',
    'Tr.heim',
    'DK1',
    'SE1',
]

BUTTON_TEST_SITE_CONTROLPLAN_PLAN_NAME = [
    ['/test?testsite=controlplans&plan_name=example_controlplan', 'example_controlplan'],
    ['/test?testsite=controlplans&plan_name=example_elspot', 'example_elspot'],
]

BUTTON_TEST_SITE_ELSPOT_REGION = [
    ['/test?testsite=elspot&region=Bergen', 'Bergen'],
    ['/test?testsite=elspot&region=DK1', 'DK1'],
    ['/test?testsite=elspot&region=DK2', 'DK2'],
    ['/test?testsite=elspot&region=EE', 'EE'],
    ['/test?testsite=elspot&region=FI', 'FI'],
    ['/test?testsite=elspot&region=Kr.sand', 'Kr.sand'],
    ['/test?testsite=elspot&region=LT', 'LT'],
    ['/test?testsite=elspot&region=LV', 'LV'],
    ['/test?testsite=elspot&region=Molde', 'Molde'],
    ['/test?testsite=elspot&region=Oslo', 'Oslo'],
    ['/test?testsite=elspot&region=SE1', 'SE1'],
    ['/test?testsite=elspot&region=SE2', 'SE2'],
    ['/test?testsite=elspot&region=SE3', 'SE3'],
    ['/test?testsite=elspot&region=SE4', 'SE4'],
    ['/test?testsite=elspot&region=SYS', 'SYS'],
    ['/test?testsite=elspot&region=Tr.heim', 'Tr.heim'],
    ['/test?testsite=elspot&region=Troms%C3%B8', 'Tromsø'],
]
