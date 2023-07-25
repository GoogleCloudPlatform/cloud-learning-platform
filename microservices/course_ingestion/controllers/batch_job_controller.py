"""controller for learning content level"""
from services.batch_job import (get_job_status,
  delete_batch_job, remove_job_and_update_status)

#pylint: disable=broad-exception-raised
class BatchJobController():
  """controller class for Job"""
  @staticmethod
  def get_job_status_controller_method(job_name):
    """controller method to get Job status"""

    return get_job_status(job_name)

  @staticmethod
  def delete_batch_job_controller_method(job_name):
    """controller method to get Job status"""
    if job_name:
      return delete_batch_job(job_name)
    else:
      raise Exception("Job name is required")

  @staticmethod
  def update_state_and_remove_job(job_name):
    """controller method to get Job status"""
    if job_name:
      return remove_job_and_update_status(job_name)
    else:
      raise Exception("Job name is required")
