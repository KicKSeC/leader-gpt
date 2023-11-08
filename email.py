import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def create_smtp(id, pwd, server="naver"):
    if server == "google":
        smtp_info = dict(
            smtp_user = id,
            smtp_password = pwd,  # 보내는 사람 이메일 비밀번호
            smtp_server = "smtp.gmail.com", 
            smtp_port = 587
        )
    elif server == "naver":
        smtp_info = dict(
            smtp_user = id,
            smtp_password = pwd,  # 보내는 사람 이메일 비밀번호
            smtp_server = "smtp.naver.com", 
            smtp_port = 587
        )
        
    return smtp_info
    

def send(from_email, pwd, to_email, subject, content, file_path=None, server="naver"):
    """이메일 발송을 시도하고 발송 결과를 문자열로 반환한다."""
    msg = MIMEMultipart("alternative") 
    msg["Subject"] = subject 
    msg["From"] = from_email 
    msg["To"] = to_email 

    msg.attach(MIMEText(content, "plain"))

    if file_path:
        attachment = MIMEBase("application", "octet-stream")
        try:
            with open(file_path, "rb") as f:
                attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=file_path)
            msg.attach(attachment)
        except Exception as e:
            print(f'Failed to attach file: {e}')

    smtp_info = create_smtp(from_email, pwd, server)
    
    with smtplib.SMTP(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
        server.starttls() 
        try:
            server.login(smtp_info["smtp_user"], smtp_info["smtp_password"]) 
            response = server.sendmail(msg['from'], msg['to'], msg.as_string()) 
        except smtplib.SMTPException:
            error_msg = ""
            error_msg += "잘못된 이메일 로그인 정보가 입력되었거나 허가되지 않은 접근입니다" 
            if server == "naver":
                error_msg += "\n허가되지 않은 접근의 경우 이를 허용하기 위해 아래 링크를 참조하십시오.\n" 
                error_msg += "https://wikidocs.net/35963"
            
            return error_msg
        if not response:
            return "메세지가 성공적으로 발송되었습니다"
        else:
            return "메세지가 정상적으로 발송되지 못하였습니다"
