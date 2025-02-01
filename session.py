from flask import session

# セッションにアンケート結果を保存
def save_survey_data(age, gender, skin_issues):
    session['age'] = age
    session['gender'] = gender
    session['skin_issues'] = skin_issues

# セッションからアンケート結果を取得
def get_survey_data():
    age = session.get('age', '')
    gender = session.get('gender', '')
    skin_issues = session.get('skin_issues', [])
    return age, gender, skin_issues

