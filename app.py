from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'

jobs_database = [
    {
        "title": "Python Developer", 
        "company": "Tech Corp", 
        "salary": "500,000 AMD", 
        "job_type": "Full-time", 
        "category": "Ծրագրավորում", 
        "experience": "Junior", 
        "description": "Looking for a junior dev."
    },
    {
        "title": "UI/UX Designer", 
        "company": "Creative Agency", 
        "salary": "400,000 AMD", 
        "job_type": "Remote", 
        "category": "Դիզայն", 
        "experience": "Middle", 
        "description": "Experience with Figma is required."
    }
]

# Այժմ բազայում ամեն օգտատիրոջ տակ կպահենք իր ամբողջական տվյալները (dictionary)
users_database = {}

@app.route('/')
def index():
    return render_template('index.html', jobs=jobs_database)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        company = request.form.get('company')
        salary = request.form.get('salary')
        
        # Վերցնում ենք նոր դաշտերը
        job_type = request.form.get('job_type')
        category = request.form.get('category')
        experience = request.form.get('experience')
        
        description = request.form.get('description')
        
        # Ավելացնում ենք բոլորը նոր աշխատանքի մեջ
        new_job = {
            "title": title,
            "company": company,
            "salary": salary,
            "job_type": job_type,
            "category": category,
            "experience": experience,
            "description": description
        }
        
        jobs_database.append(new_job)
        return redirect(url_for('index'))
        
    return render_template('add_job.html')

# ԹԱՐՄԱՑՎԱԾ ԳՐԱՆՑՈՒՄ
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users_database:
            return "Այս օգտանունով մարդ արդեն գրանցված է:"
        
        # Պահում ենք բոլոր տվյալները միասին
        users_database[username] = {
            "password": password,
            "full_name": full_name,
            "email": email,
            "phone": phone
        }
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Քանի որ կառուցվածքը փոխվեց, հիմա ստուգում ենք users_database[username]['password']
        if username in users_database and users_database[username]['password'] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "Սխալ օգտանուն կամ գաղտնաբառ:"
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)