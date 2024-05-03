from flask import Flask, render_template, request, redirect, url_for
import boto3

# AWS credentials
ACCESS_KEY = 'ACCESS KEY'
SECRET_KEY = 'SECRET KEY'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get details from the form
        contact_info = request.form['contact_info']
        objective = request.form.get('objective', '')
        work_experience = request.form['work_experience']
        education = request.form['education']
        skills = request.form['skills']
        certifications = request.form.get('certifications', '')
        awards = request.form.get('awards', '')
        publications = request.form.get('publications', '')
        volunteer_experience = request.form.get('volunteer_experience', '')
        memberships = request.form.get('memberships', '')

        # Format details as a resume
        resume = f"Contact Information:\n{contact_info}\n\n"
        if objective:
            resume += f"Objective:\n{objective}\n\n"
        resume += f"Work Experience:\n{work_experience}\n\n"
        resume += f"Education:\n{education}\n\n"
        resume += f"Skills:\n{skills}\n\n"
        if certifications:
            resume += f"Certifications:\n{certifications}\n\n"
        if awards:
            resume += f"Awards and Honors:\n{awards}\n\n"
        if publications:
            resume += f"Publications:\n{publications}\n\n"
        if volunteer_experience:
            resume += f"Volunteer Experience:\n{volunteer_experience}\n\n"
        if memberships:
            resume += f"Professional Memberships:\n{memberships}\n\n"

        # Store resume in a txt file in S3 Bucket
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        bucket_name = 'BUCKET NAME'
        file_name = 'resume.txt'
        s3.put_object(Body=resume, Bucket=bucket_name, Key=file_name)

        return redirect(url_for('download_resume'))

    return render_template('index.html')

@app.route('/download')
def download_resume():
    # Generate a presigned URL to download the resume from S3 Bucket
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    bucket_name = 'BUCKET NAME'
    file_name = 'resume.txt'
    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_name}, ExpiresIn=3600)

    return render_template('download.html', download_url=url)

if __name__ == '__main__':
    app.run(debug=True)
