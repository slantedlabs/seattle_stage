from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import sys
import getpass

class Command(BaseCommand):
  help = 'Create new user'

  def add_arguments(self, parser):
    parser.add_argument('-n', '--name',
        default='',
        type=str)
    parser.add_argument('-p', '--password',
        default='',
        type=str)
    parser.add_argument('-e', '--email',
        default='',
        type=str)
    parser.add_argument('--noinput',
        default=False,
        type=bool)


  def handle(self, *args, **options):
    name = options['name']
    password = options['password']
    email = options['email']
    noinput = options['noinput']

    if not name and not noinput:
      name = raw_input("Username: ")
    if not name:
      print("Error: username cannot be empty")
      sys.exit(1)

    if not password and not noinput:
      password = getpass.getpass()
    if not password:
      print("Error: password cannot be blank")
      sys.exit(1)

    if not noinput:
      confirm_password = getpass.getpass()
      if not confirm_password == password:
        print("Error: passwords do not match")
        sys.exit(1)

    if not email and not noinput:
      email = raw_input("Email: ")

    user = User.objects.create_user(username=name,
        email=email,
        password=password)

    print("New user '{}' created.".format(user.username))

