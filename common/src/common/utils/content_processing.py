""" Helper Classes for Content Upload """
import os
from glob import glob
import pathlib
from zipfile import ZipFile
from common.utils.errors import (ValidationError,
                                  InternalServerError)

# pylint: disable = line-too-long,consider-using-join,invalid-name
FOLDER_NAMES_TO_EXCLUDE = ["Templates", "Resources"]

ALLOWED_CONTENT_TYPES = [
  "application/ogg",
  "application/pdf",
  "application/xhtml+xml",
  "application/xml",
  "application/zip",
  "application/x-zip-compressed",
  "audio/mpeg",
  "audio/x-ms-wma",
  "audio/vnd.rn-realaudio",
  "audio/x-wav",
  "image/gif",
  "image/jpeg",
  "image/png",
  "image/tiff",
  "image/svg+xml",
  "text/css",
  "text/csv",
  "text/html",
  "text/javascript",
  "text/plain",
  "text/xml",
  "video/mpeg",
  "video/mp4",
  "video/webm",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

class ContentValidator:
  """Class for content validators"""
  def __init__(self):
    pass

  def isValidSCORMPackage(self, resource_type, file_path):
    # TODO
    pass

  def checkEntryPointExists(self, src_path, relative_entry_point):
    """
            Check if the entry point exists in the extracted contents of the zip
            src_path: `str`
                This is the path to the folder where entry point is to be checked
            relative_entry_point: `str`
                This is the path to the entrypoint of the package inside
                the root folder of the content
        """
    return os.path.exists(f"{src_path}/{relative_entry_point}")

  def checkResourceTypeAndExtension(self, resource_type, extension):
    """Function to check resource type and extension"""
    file_extensions = ["pdf", "image", "html", "video", "docx"]
    if resource_type in file_extensions:
      if resource_type == "pdf" and extension in ["pdf", "PDF"]:
        return True
      elif resource_type == "video" and extension in ["mp4"]:
        return True
      elif resource_type == "html" and extension in ["HTML", "html"]:
        return True
      elif resource_type == "docx" and extension in ["docx", "DOCX"]:
        return True
    else:
      if resource_type in ["html_package", "scorm"
                          ] and extension in ["zip", "ZIP"]:
        return True

    return False

  def checkExtensionAndContentHeader(self, content_header, extension):
    """Function to check extension and content header"""
    if content_header.split("/")[-1] == extension.lower():
      return True
    elif content_header == "text/html" and extension.lower() in ["htm","html"]:
      return True
    elif content_header == "text/plain" and extension.lower() in ["txt"]:
      return True
    elif content_header == "application/x-zip-compressed" and extension.lower() == "zip":
      return True
    elif content_header == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" and extension.lower() == "docx":
      return True

    return False

  def isValidHTMLPackage(self, resource_type, file_path):
    # TODO
    pass

  def isValidMadcapExport(self, folder_path, folder_name, check_srl=False):
    """
        A valid madcap export must have the following files:
        1. Default.htm
            This will be entrypoint of the entire madcap export.
        2. Content Folder
            This will contain other html files, nested in other folders.
    """
    default_htm = glob(f"{folder_path}/**/Default.htm", recursive=True)
    if len(default_htm)==0:
      msg = f"{folder_name} is not a valid Madcap Export. Default.htm file was not found."
      return False, msg

    content_folder_data = glob(f"{folder_path}/**/Content/**/**.htm", recursive = True)

    # For each item to be excluded, reduce the search space
    # Filter out only the required .htm files
    allowed_files = content_folder_data
    for item in FOLDER_NAMES_TO_EXCLUDE:
      temp_files = []
      for file in allowed_files:
        if item not in file:
          temp_files.append(file)
      allowed_files = temp_files

    content_folder_data = allowed_files

    if len(content_folder_data) == 0:
      msg = f"{folder_name} is not a valid Madcap Export. No .htm files found in Content folder"
      return False, msg

    if check_srl is True:
      required_srl_files = []
      for file in content_folder_data:
        if "SRL" in file.split("/")[-1]:
          required_srl_files.append(file)

      if len(required_srl_files) == 0:
        msg = f"""{folder_name} is not a valid SRL Madcap Export. The .htm files do not contain "SRL" prefix."""
        return False, msg

    return True, None

class FileUtils:
  """Class for file handling"""
  def __init__(self):
    pass

  def zip(self, file_path_list, dest_path, output_filename):
    """Function to zip given files"""
    # Validate files
    missing_files_list = []
    for file in file_path_list:
      if not os.path.exists(file):
        missing_files_list.append(file)

    if len(missing_files_list) != 0:
      # Generate Error log
      err_msg = f"Total missing files: {len(missing_files_list)}"
      err_msg = "Following files were not found: \n"
      for file in missing_files_list:
        err_msg += f"{file} \n"

      raise InternalServerError(err_msg)

    # Create zip
    zip_destination = f"{dest_path}/{output_filename}"

    with ZipFile(zip_destination, "w") as zip_object:
      for file in file_path_list:
        zip_object.write(file)

    return zip_destination

  def unzipPackage(self, file_path, dest_path):
    with ZipFile(file_path, "r") as zObject:
      zObject.extractall(path=dest_path)

  def deleteFile(self, filepath):
    if os.path.exists(filepath):
      os.remove(filepath)
      print(f"File at path {filepath} deleted successfully")
      return
    print(f"File at path {filepath} does not exist")

  def deleteFolder(self, dir_name):
    """Function to delete folder"""
    if os.path.exists(dir_name):
      folder = pathlib.Path(dir_name)
      all_children = list(folder.rglob("*"))
      for item in all_children:
        if os.path.isfile(item):
          os.remove(item)
          print(f"File at path {item} deleted successfully")
        elif os.path.isdir(item):
          self.deleteFolder(item)
          print(f"Folder at path {item} deleted successfully")
      os.rmdir(dir_name)
    else:
      print(f"Folder at path {dir_name} was not found")

  def getContentFolderFiles(self, dir_name):
    """Function to get files in folder"""
    if os.path.exists(dir_name):
      content_folder_htm_files = []

      folder = pathlib.Path(dir_name)
      all_children = list(folder.rglob("*"))
      for item in all_children:
        if "Content" in str(item) and ".htm" in str(item):
          content_folder_htm_files.append(str(item))

      return content_folder_htm_files
    else:
      raise ValidationError(f"Folder at path {dir_name} was not found")
