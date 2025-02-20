import regex as re
from email.utils import parseaddr


def is_email(email):
    email = email.replace(" ", "")
    email = email.replace('[at]', '@')
    email = email.replace('[@]', '@')
    email = email.replace('[dot]', '.')
    email = email.replace('(at)', '@')
    email = email.replace('(dot)', '.')
    email = email.replace('(@)', '@')


    a = re.compile(r'[^@]+(@)[^@]+\.[^@]+')

    if(a.fullmatch(email)):
        try:
            the_email = parseaddr(email)[1]
        except Exception as e:
            the_email = ''
    
        if the_email == '':
            return False
        else:
            return True
    return False


def is_website(website):
    a = re.compile(r'(www\.)?.+\.(com|io|or|ai|games|org|(.)*).*')
    return a.fullmatch(website)
