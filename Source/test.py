from prefect import Flow

validation_config = {
    "discrepancy_threshold": {
        "low": 0.9,
        "high": 1.9
    },
    "events": [{
        "aut": ["event_type:pv"],
        "amdp": "AQFERPAGEVIEW"
    },
        {
        "aut": ["event_type:imp"],
        "amdp": "AQFERIMPRESSION"
    }
    ]}

validation_config_1 = {
    "discrepancy_threshold": {
        "low": 0.9,
        "high": 1.9
    },
    "events": [{
        "aut": ["event_type:pv", "event_type:imp"],
        "amdp": "AQFERPAGEVIEW"
    }
    ]}

query_result_1 = {'metrics': [{'data_channel': 'AQFERPAGEVIEW', 'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:pv',
                                  'record_schema': 'aut', 'record_count': 100},
                              {'data_channel': 'event_type:imp', 'record_schema': 'aut', 'record_count': 100}]}
query_result_2 = {'metrics': [{'data_channel': 'AQFERPAGEVIEW', 'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:pv', 'record_schema': 'aut', 'record_count': 100}]}
query_result_3 = {'metrics': [{'data_channel': 'AQFERPAGEVIEW', 'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:pv',
                                  'record_schema': 'aut', 'record_count': 100},
                              {'data_channel': 'AQFERIMPRESSION',
                                  'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:imp', 'record_schema': 'aut', 'record_count': 100}]}
query_result_4 = {'metrics': [{'data_channel': 'AQFERPAGEVIEW', 'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:pv',
                                  'record_schema': 'aut', 'record_count': 100},
                              {'data_channel': 'AQFERIMPRESSION',
                                  'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:imp', 'record_schema': 'aut', 'record_count': 99}]}
query_result_5 = {'metrics': [{'data_channel': 'AQFERPAGEVIEW', 'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:pv',
                                  'record_schema': 'aut', 'record_count': 99},
                              {'data_channel': 'AQFERIMPRESSION',
                                  'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:imp', 'record_schema': 'aut', 'record_count': 98}]}
query_result_6 = {'metrics': [{'data_channel': 'AQFERPAGEVIEW', 'record_schema': 'amdp', 'record_count': 100},
                              {'data_channel': 'event_type:pv',
                                  'record_schema': 'aut', 'record_count': 50},
                              {'data_channel': 'event_type:imp', 'record_schema': 'aut', 'record_count': 50}]}
query_result_7 = {}

validate_aut_amdp = ValidateAutAmdp()


with Flow("test-validate-aut-amdp") as flow:
    t1 = validate_aut_amdp(validation_config, query_result_1)
    t2 = validate_aut_amdp(validation_config, query_result_2)
    t3 = validate_aut_amdp(validation_config, query_result_3)
    t4 = validate_aut_amdp(validation_config, query_result_4)
    t5 = validate_aut_amdp(validation_config, query_result_5)
    t6 = validate_aut_amdp(validation_config_1, query_result_6)
    t7 = validate_aut_amdp(validation_config, query_result_7)

state = flow.run()
assert state.result[t1].is_failed()
assert state.result[t2].is_successful()
assert state.result[t3].is_successful()
assert state.result[t4].is_failed()
assert state.result[t4].result.flag == True
assert state.result[t5].is_failed()
assert state.result[t6].is_successful()
assert state.result[t7].is_successful()

