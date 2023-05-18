"""sample feature to test environment.py"""

import sys
import behave
sys.path.append("../")
from setup import delete_user_from_db, delete_user

# 1. This checks if everything is implemented correctly in environment.py
# 2. It also cleans up the User data from Firestore that was created for Authentication
# 3. It is run twice in E2E workflow -
# first time, before running all the E2Es to test the environment.py file, as BehaveX cannot catch errors in environment.py.
# second time, after running all the E2Es to cleanup the User data. 
@behave.given("environment.py is correctly implemented")
def step_1(context):
  delete_user()
  delete_user_from_db()
