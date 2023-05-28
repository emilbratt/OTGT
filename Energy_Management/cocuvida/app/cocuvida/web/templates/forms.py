from cocuvida.sqldatabase import controlplans as sql_controlplans
from cocuvida.sqldatabase import elspot as sql_elspot


async def controlplan_upload() -> bytes:
    html = b'''
    <p>Upload</p>
    <form method="POST" action="" enctype="multipart/form-data">
        <input type="file"
               id="upload_control_plan"
               name="control_plan"
               accept=".yml,.yaml"
               required />
        <br>
        <label for="secret">Secret:</label>
        <input type="password"
               id="secret"
               name="secret"
               required />
        <button type="submit"
                name="submit"
                value="upload">Upload
        </button>
    </form>
    <hr>
    '''
    return html

async def controlplan_options() -> bytes:
    plan_names = await sql_controlplans.list_plan_names()
    if len(plan_names) < 1:
        return b''
    html = '''
    <p>Options</p>
    <form method="POST" action="" enctype="multipart/form-data">
    <select id="control_plan_options" name="plan_name">
    '''
    for name in plan_names:
        html += f'<option value="{name}">{name}</option>'
    html += '''
    </select><br>
    <label for="secret">Secret:</label>
    <input type="password"
           id="secret"
           name="secret"
           required />
    <button type="submit" name="submit" value="schedule">Schedule</button>
    <button type="submit" name="submit" value="show">Show</button>
    <button type="submit" name="submit" value="download">Download</button>
    <button type="submit" name="submit" onclick="return confirm('Confirm deletion');" value="delete">Delete</button>
    </form>
    <hr>
    '''
    return html.encode()

async def upload_elspot_dayahead() -> bytes:
    html = b'''
    <p>Upload dayahead json</p>
    <form method="POST" action="" enctype="multipart/form-data">
        <input type="file"
               id="upload_elspot_raw"
               name="elspot_dayahead_json"
               accept=".json    "
               required />
        <br>
        <button type="submit" name="submit" value="upload_elspot_dayahead">Upload</button>
    </form>
    <hr>
    '''
    return html

async def select_elspot_dayahead() -> bytes:
    dates = await sql_elspot.list_elspot_raw_dates()
    if dates == []:
        return b''
    html = '''
    <p>Select dayahead from database</p>
    <form method="POST" action="" enctype="multipart/form-data">
    <select id="elspot_dayahead_date" name="elspot_dayahead_date">
    '''
    for date in dates:
        html += f'<option value="{date}">{date}</option>'
    html += '''
    </select><br>
    <button type="submit" name="submit" value="select_elspot_dayahead">Select</button>
    </form>
    <hr>
    '''
    return html.encode()

async def download_elspot_dayahead() -> bytes:
    html = '''
    <p>Download latest dayahead from NordPool</p>
    <form method="POST" action="" enctype="multipart/form-data">
    <select id="elspot_dayahead_date" name="elspot_dayahead_currency">
        <option value="DKK">DKK</option>'
        <option value="EUR">EUR</option>'
        <option value="NOK">NOK</option>'
        <option value="SEK">SEK</option>'
    </select><br>
    <button type="submit" name="submit" value="download_elspot_dayahead">Download</button>
    </form>
    <hr>
    '''
    return html.encode()
