import requests
import time, sys, os, datetime

path = sys.argv[1]

if os.path.isfile(path):
    with open(path) as f:
        l = [s.rstrip() for s in f.readlines()]
        try:
            userid = [s for s in l if s.startswith('USERID=')][0].lstrip('USERID=')
        except IndexError:
            print('User ID is not set.\nユーザーIDが設定されていません。\nUSERID=<userid>')
            sys.exit(1)
        try:
            password = [s for s in l if s.startswith('PASSWORD=')][0].lstrip('PASSWORD=')
        except IndexError:
            print('Password is not set.\nパスワードが設定されていません。\nPASSWORD=<password>')
            sys.exit(1)
        try:
            userid_form = [s for s in l if s.startswith('USERID_FORM=')][0].lstrip('USERID_FORM=')
        except IndexError:
            userid_form = 'userid'
            print('User ID Form is not set. Use the default "userid".\nユーザーIDフォームが設定されていません。デフォルトの"userid"を使用します。\nUSERID_FORM=<userid>')
        try:
            password_form = [s for s in l if s.startswith('PASSWORD_FORM=')][0].lstrip('PASSWORD_FORM=')
        except IndexError:
            password_form = 'password'
            print('Password Form is not set. Use the default "password".\nパスワードフォームが設定されていません。デフォルトの"password"を使用します。\nPASSWORD_FORM=<password>')
        try:
            try_url = [s for s in l if s.startswith('TRYURL=')][0].lstrip('TRYURL=')
        except IndexError:
            try_url = 'http://captive.apple.com'
            print('Try URL is not set. Use the default "http://captive.apple.com".\n。トライURLが設定されていません。デフォルトの"http://captive.apple.com"を使用します。\nTRYURL=<url>')
        try:
            interval = float([s for s in l if s.startswith('INTERVAL=')][0].lstrip('INTERVAL='))
        except IndexError:
            interval = float(0.1)
            print('Try Interval is not set. Use the default "0.1".\nトライ間隔が設定されていません。デフォルトの"0.1"を使用します。\nINTERVAL=<seconds>')
        except ValueError:
            interval = float(0.1)
            print('The try interval is not set correctly. Only numbers (seconds) can be used. Use the default "0.1".\nトライ間隔が正しく設定されていません。数字（秒）のみが使用できます。デフォルトの"0.1"を使用します。\nINTERVAL=<seconds>')
    print('The configuration file has been read correctly.\n設定ファイルが正しく読み込まれました。')
else:
    print('Please specify the correct configuration file.\n正しい設定ファイルを指定してください。')
    sys.exit(1)

payload = {userid_form: userid, password_form: password}

def get_redirect_url(url):
    try:
        resp = requests.head(url, allow_redirects=False)
        if 'Location' in resp.headers:
            return resp.headers['Location']
        return None
    except requests.exceptions.RequestException as e:
        return None


while True:
    redirect_url = get_redirect_url(try_url)
    if redirect_url is not None:
        try:
            print(redirect_url)
            s = requests.post(redirect_url, data=payload)
        except requests.exceptions.RequestException as e:
            pass
        else:
            print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M') + ' Sucsess')
    else:
        time.sleep(interval)
        redirect_url = ''