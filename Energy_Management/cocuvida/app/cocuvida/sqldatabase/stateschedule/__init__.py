from cocuvida.sqldatabase import connect


QUERIES = {
    'insert_state': 'INSERT INTO state_schedule (plan_name, state_value) VALUES (?, ?)',
    'insert_state_and_timestamp': 'INSERT INTO state_schedule (plan_name, state_value, state_timestamp) VALUES (?, ?, ?)',
    'update_state': 'UPDATE state_schedule  SET plan_data = ?  WHERE plan_name = ?',
    'show_state': 'SELECT plan_data FROM state_schedule WHERE plan_name = ? AND state_timestamp = ?',
    'delete_state': 'DELETE FROM state_schedule WHERE plan_name = ? AND state_timestamp = ?',
    'list_states': 'SELECT plan_name FROM state_schedule',
}
