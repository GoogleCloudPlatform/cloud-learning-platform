"""class and methods for routes handling."""
import traceback
from routes.base_handler import BaseHandler
from common.utils.logging_handler import Logger
from controllers.batch_job_controller import BatchJobController

# pylint: disable=abstract-method
# pylint: disable=unused-argument
# pylint: disable=redefined-builtin
class BatchJobHandler(BaseHandler):
  """Class for job handler"""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      job_name = args[-1]
      response = BatchJobController.get_job_status_controller_method(
        job_name)
      if job_name:
        response_message = "Batch Job status: {}".format(response["status"])
      else:
        response_message = "Successfully fetched batch jobs"
      return self.send_json(
        status=200,
        success=True,
        message=response_message,
        response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  def delete(self, *args, **kwargs):
    """Method for delete request."""
    try:
      job_name = args[-1]
      BatchJobController.delete_batch_job_controller_method(job_name)
      return self.send_json(
          status=200,
          success=True,
          message="A job with name {} has been deleted".format(job_name))

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  def put(self, *args, **kwargs):
    """Method for put request."""
    try:
      job_name = args[-1]
      return self.send_json(
          status=200,
          success=True,
          message="A job with name {} has been aborted".format(job_name),
          response=BatchJobController
          .update_state_and_remove_job(job_name),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)
