import click
from email.message import EmailMessage
from mimetypes import guess_type
import pathlib
import smtplib
from sys import exit


@click.command()
@click.argument(
    'packaged-grading-folder',
    type=click.Path(exists=True, file_okay=False,
                    readable=True, resolve_path=True)
)
@click.option(
    '--username', '-u',
    type=click.STRING, prompt=True,
    help="""
    Your NAU username that you use to log in to the CAS.
    """
)
@click.option(
    '--password', '-p',
    type=click.STRING, prompt=True, hide_input=True,
    help="""
    Your NAU password that you use to log in to the CAS.
    """
)
@click.option(
    '--from-address', '-f',
    type=click.STRING, prompt=True,
    help="""
    Your NAU faculty e-mail address.
    """
)
@click.option(
    '--subject', '-s',
    type=click.STRING, prompt=True,
    help="""
    The subject line for the e-mailed grading zipfiles.
    """
)
@click.option(
    '--message', '-m',
    type=click.STRING, prompt=True,
    help="""
    The message to be included with the e-mailed grading zipfiles.
    """
)
def send(packaged_grading_folder,
         username, password, from_address, subject, message):
    """
    The zip files generated by the 'divvy package' command which are contained
    in the PACKAGED_GRADING_FOLDER are sent to the student designated in the
    name of the zip file via your NAU iris e-mail.
    """
    # Connect to the server
    with smtplib.SMTP('iris.nau.edu', 587) as iris:
        try:
            iris.ehlo()
            iris.starttls()
        except Exception as connection_err:
            print("Something went wrong connecting to iris "
                  "(not login credential related):")
            print(connection_err)
            exit(1)
        try:
            iris.login(username, password)
        except Exception as login_err:
            print("Something went wrong with your login credentials")
            print(login_err)
            exit(1)

        zip_paths = list(pathlib.Path(packaged_grading_folder).iterdir())
        print(f"Attempting to send {len(zip_paths)} emails:")
        unsuccessful_sends = []
        for zip_path in sorted(zip_paths, key=lambda path: path.name):
            student_email = zip_path.name.split('__')[0] + '@nau.edu'
            msg = EmailMessage()
            msg['To'] = student_email
            msg['From'] = from_address
            msg['Subject'] = subject
            msg.set_content(message)
            ctype, _ = guess_type(zip_path)
            maintype, subtype = ctype.split('/')
            with open(zip_path, 'rb') as attachment_file:
                msg.add_attachment(attachment_file.read(),
                                   maintype=maintype,
                                   subtype=subtype,
                                   filename=zip_path.name)
            print(f"\tSending to {student_email} ...\t", end="")
            send_result = iris.send_message(msg)
            if send_result == {}:
                print("SUCCESS")
            else:
                print("FAILURE")
                unsuccessful_sends.append(student_email)

    print(f"In {len(zip_paths)} emails, there were {len(unsuccessful_sends)} "
          f"failures to send{':' if unsuccessful_sends else '.'}")
    for email_address in unsuccessful_sends:
        print(f"\t{email_address}")
