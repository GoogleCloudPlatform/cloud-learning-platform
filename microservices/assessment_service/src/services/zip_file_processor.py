"""Script for creating zip files"""
from common.utils.content_processing import (FileUtils)
from config import (TEMP_FOLDER)

fileHandler = FileUtils()


def create_zip_file(file_list, output_filename):
  """
    This function will create a zip file from a list of provided
    local files
    -------------------------------------------------------------
    Input:
        local_file_path_list `list[str]`: List of file locations
                            in the temp folder to be zipped
        output_filename `str`: Name of the output file
    -------------------------------------------------------------
    Output:
        zip_file_location `str`: Location of the new zip file
    """
  dest_path = f"{TEMP_FOLDER}"

  zip_location = fileHandler.zip(
      file_path_list=file_list,
      dest_path=dest_path,
      output_filename=output_filename)
  return zip_location
