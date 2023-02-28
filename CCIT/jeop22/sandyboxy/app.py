import subprocess
from flask import Flask, redirect, render_template, request, send_file, session
from flask import flash, redirect, url_for
import tempfile
import os
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET', os.urandom(16))
app.config['FLAG'] = os.environ.get('FLAG', 'CCIT{DUMMY_FLAG}')

class Program:

    def __init__(self, code:str) -> None:
        self.code = code
    
    def execute(self):
        if len(self.code) > 200:
            return False
        parsed_code = ''
        for line in self.code.split('\\n'):
            if '(' in line:
                continue
                
            parsed_code += line

        tmpfile = tempfile.NamedTemporaryFile('w', delete=False)
        file_name = tmpfile.name

        template = """
code = '''
{}
'''
glob = {{}} # no globals!
loc = {{}}  # no locals!
eval(compile(code, '<string>', 'exec'), glob, loc)  
        """
        
        parsed_code = parsed_code.replace("'","")
        tmpfile.write(template.format(parsed_code))
        tmpfile.close()
        os.chmod(file_name, 0o755)
        p = subprocess.Popen('python '+ file_name, shell=True, user='web', group='web')
        p.wait(2)
        
        


@app.get('/')
def index():
    if not session.get('code', False):
        return render_template('index.html', code='')
    
    code = session['code']
    return render_template('index.html', code=code)

@app.get('/source')
def source():
    return send_file(__file__)

@app.post('/')
def save_code():
    code = request.form.get('code', False)

    if not code:
        flash('You have to post some code in order to save it!')
        return redirect(url_for('index'))
    
    session['code'] = code
    return redirect(url_for('index'))

@app.get('/execute')
def execute():
    code = session.get('code', False)
    if not code:
        flash('You have to post some code in order to save it!')
        return redirect(url_for('index'))

    program = Program(code)
    try:
        program.execute()
    except:
        output = traceback.format_exc()
    else:
        output = 'Executed! no error so far!'    

    return render_template('execute.html', output=output)


if __name__ == '__main__':
    app.run('localhost', 5000, True)