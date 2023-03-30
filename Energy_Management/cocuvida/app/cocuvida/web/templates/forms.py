from cocuvida.sqldatabase.controlplans import list_plan_names as sql_list_plan_names


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
    plan_names = await sql_list_plan_names()
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