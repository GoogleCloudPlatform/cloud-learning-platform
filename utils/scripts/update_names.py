# disabling for linting to pass
# pylint: disable=unspecified-encoding,missing-module-docstring,broad-exception-raised,broad-exception-caught,invalid-name,unused-variable
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.models import User
import csv


def main():
  print("Started Script")
  # Use a service account.
  cred = credentials.Certificate("asu-prod-key.json")
  print("Cred", cred)
  firebase_admin.initialize_app(cred)

  db = firestore.client()
  print("User.collection name", User.collection_name)
  enrollment_ref = db.collection(User.collection_name)
  docs = enrollment_ref.stream()
  print("------------------------------------------------")
  with open("MAT142_Spring_B_2024_roster_names11.csv", mode="r") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
      print(lines)
      user = User.find_by_email(lines[0])
      print("User is", user, lines[0])
      if user is not None:
        if user.first_name != lines[1] or user.last_name != lines[2]:

          user.first_name = lines[1]
          user.last_name = lines[2]
          user.update()
          with open("mat_springb_2024.txt", "w") as out_file:
            out_file.write(
                f"{user.email}, {user.first_name}, {user.last_name}\n")
            print("File write In updated Users", user.email)
        else:
          with open("mat_springb_not_updated_users2024.txt", "w") as out_file:
            out_file.write(
                f"{user.email}, {user.first_name}, {user.last_name}\n")
            print("File write In NOT updated Users", user.email)

      else:
        print("User Not found", lines[0])


if __name__ == "__main__":
  main()
