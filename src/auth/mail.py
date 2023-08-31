from email.message import EmailMessage
from config import EMAIL_SEND

def get_email_template(username: str, user_email: str, code: int):
    email = EmailMessage()
    email['Subject'] = 'Код верификации Pinterest'
    email['From'] = EMAIL_SEND
    email['To'] = user_email

    code_to_list = list(str(code))

    email.set_content(
        '<div>'
            f'<h1 style="text-align: center;">Здравствуйте, {username}, вот Ваш код верификации:</h1>'
            '<div style="padding: 20px; display: flex; justify-content: center; align-items: center; gap: 5px;">'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[0]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[1]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[2]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[3]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[4]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[5]}</h1>'
                '</div>'
            '</div>'
        '</div>',
        subtype='html'
    )
    return email

