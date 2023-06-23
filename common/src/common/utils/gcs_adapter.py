"""Module for GCS Services"""
import os
import gcsfs
import traceback
import logging
import glob
from io import StringIO
import csv
from datetime import timedelta
from google.cloud import storage
from common.utils.logging_handler import Logger

# pylint: disable=consider-using-f-string, logging-format-interpolation
# pylint: disable = broad-exception-raised

gcs_bucket = os.environ.get("GCP_PROJECT")


class GcsCrudService:
  """
  Class for GCS CRUD Operation
  """

  def __init__(self, bucket_name, signurl_sa_path=None):
    if signurl_sa_path:
      self.storage_client = storage.Client.from_service_account_json(
          signurl_sa_path)
    else:
      self.storage_client = storage.Client()
    self.bucket_name = bucket_name
    self.bucket = self.storage_client.bucket(bucket_name)

  def fetch_all_blobs(self, prefix=None) -> list:
    """
    Function is used to fetch all the blobs from the bucket
    :prefix: string
    """
    if prefix is not None:
      blobs = self.storage_client.list_blobs(
          self.bucket_name, prefix=f"{prefix}/")
    else:
      blobs = self.storage_client.list_blobs(self.bucket_name)

    return blobs

  def upload_file_to_gcs_bucket(self,
                                file_name: str,
                                file_body: str,
                                parent_folder_name=None):
    """
    Upload new file to GCS bucket
    :param file_name: string
    :param file_body: string
    :param parent_folder_name: string (optional)
    :return: string
    """
    folder_name = file_name.split(".")[0]
    fs = gcsfs.GCSFileSystem(project=self.bucket_name)

    if parent_folder_name is not None:
      folder_path = f"{self.bucket_name}/{parent_folder_name}/{folder_name}/" \
                    f"{file_name}"
    else:
      folder_path = f"{self.bucket_name}/{folder_name}/{file_name}"

    with fs.open(folder_path, "wb") as f:
      f.write(file_body)
    fs.du(folder_path)

    return {"gs_path": f"gs://{folder_path}"}

  def get_blob_from_gcs_path(self, gcs_path):
    """returns blob object using gcs_path"""
    storage_client = storage.Client()
    bucket_name = gcs_path.split("gs://")[1].split("/")[0]
    blob_name = gcs_path.split(bucket_name)[-1].strip("/")
    bucket = storage_client.bucket(bucket_name)
    if not bucket:
      raise ValueError(f"Unknown path \"{gcs_path}\"")
    blob = bucket.get_blob(blob_name)
    if not blob:
      raise ValueError(f"Unknown path \"{gcs_path}\"")
    return blob

  def parse_gcs_csv_file(self, blob):
    """downloads csv from gcs and returns it as json"""
    # download file as bytes
    file_data = blob.download_as_bytes()
    byte_content = file_data
    content = byte_content.decode()
    file = StringIO(content)
    csv_reader = csv.DictReader(file, delimiter=",")
    return list(csv_reader)

  def delete_file_from_gcs_bucket(self, blob_name: str):
    """
    Delete File from the GCS bucket
    :param blob_name: path of the GCS object (string)
    :return: string
    """
    blobs = self.bucket.list_blobs(prefix=f"{blob_name}")
    for blob in blobs:
      blob.delete()
    file_path = blob_name.split("/")
    file_name = [name for name in file_path if ".pdf" in name.lower()][0]

    return f"{file_name} is deleted successfully"

  def generate_url(self, prefix, expiration_minutes=60):
    """
    Method to generate url
    """
    try:
      bucket = self.storage_client.get_bucket(self.bucket_name)
      blob = bucket.blob(prefix)
      url = blob.generate_signed_url(
          version="v4",
          # This URL is valid for 60 minutes
          expiration=timedelta(minutes=expiration_minutes),
          method="GET"  # Allow GET requests using this URL.
      )
      return url
    except Exception as err:  # pylint: disable=broad-except
      return err

  def get_bucket_folders(self, prefix, delimiter = "/"):
    """
    Method to get list of folders in bucket
    """
    if delimiter is None:
      blobs = self.storage_client.list_blobs(
          self.bucket_name,
          prefix=prefix)
      _ = [blob.name for blob in blobs]
      prefix_list = list(blobs.prefixes)
      folder_list = [x.strip("/") for x in prefix_list]
      return sorted(folder_list)
    else:
      blobs = self.storage_client.list_blobs(
          self.bucket_name,
          prefix=prefix,
          delimiter=delimiter,
          include_trailing_delimiter=True)
      _ = [blob.name for blob in blobs]
      prefix_list = list(blobs.prefixes)
      folder_list = [x.strip("/") for x in prefix_list]
      return sorted(folder_list)

  def get_files_from_folder(self,prefix, delimiter = "/"):
    """
    Method to list all the files in a folder
    """
    if delimiter is None:
      blobs = self.storage_client.list_blobs(
          self.bucket_name,
          prefix=prefix)
      blob_list = [blob.name for blob in blobs]
      return sorted(blob_list)
    else:
      blobs = self.storage_client.list_blobs(
          self.bucket_name,
          prefix=prefix,
          delimiter=delimiter,
          include_trailing_delimiter=True)
      blob_list = [blob.name for blob in blobs]
      return sorted(blob_list)

  def get_bucket_data(self, prefix):
    """
    Method to get all bucket data
    """
    blobs = self.storage_client.list_blobs(
        self.bucket_name,
        prefix=prefix,
        delimiter="/",
        include_trailing_delimiter=True)
    blob_list = []
    for blob in blobs:
      blob_dict = {}
      blob_dict["name"] = blob.name
      blob_dict["bucket"] = blob.bucket.name
      blob_dict["contentType"] = blob.content_type
      blob_dict["size"] = blob.size
      blob_dict["storageClass"] = blob.storage_class
      blob_dict["mediaLink"] = blob.media_link
      blob_dict["id"] = blob.id
      blob_dict["generation"] = blob.generation
      blob_dict["metadata"] = blob.metadata
      blob_dict["etag"] = blob.etag
      blob_list.append(blob_dict)

    prefix_list = []
    for el in sorted(list(blobs.prefixes)):
      prefix_list.append(el)

    result_dict = {}
    result_dict["prefixes"] = prefix_list
    result_dict["items"] = blob_list
    return result_dict

  def upload_file_to_bucket(self, prefix, file_name, file_path):
    """Upload file to gcs bucket

      Args:
          prefix: folder name
          file_name: name of file with extension
          file: File to be uploaded

      Returns: uri
      """
    client = storage.Client()
    bucket = client.get_bucket(self.bucket_name)
    blob = bucket.blob(f"{prefix}/{file_name}")
    blob.upload_from_filename(file_path)
    return f"gs://{self.bucket_name}/{prefix}/{file_name}"


def download_blob(base_path, destination_folder="data"):
  """Download all the files from the GCS path into a local folder."""
  storage_client = storage.Client()

  if (base_path.startswith("gs://") is not True or
      base_path.endswith("/") is True):
    logging.error("GCS path names must start with \
            gs:// and end end with a number or letter.")
    return

  logging.info("Downloading data from base path \
        in Cloud storage..Wait for the job to complete.")

  path = base_path.replace("gs://", "").split("/")

  bucket_name = path[0]
  prefix = "/".join(path[1:])
  delimiter = "/".join(path[1:])

  blobs = storage_client.list_blobs(
      bucket_name, prefix=prefix + "/", delimiter=delimiter + "/")

  for blob in blobs:
    destination_folder_path = blob.name.replace(prefix,
                                                destination_folder).rsplit(
                                                    "/", 1)[0]
    os.makedirs(destination_folder_path, exist_ok=True)
    destination_file_name = blob.name.replace(prefix, destination_folder)

    if not os.path.isfile(destination_file_name):
      if destination_file_name != (destination_folder + "/"):
        try:
          blob.download_to_filename(destination_file_name)
        except TypeError:
          logging.error("Error downloading file %s: ",
                        str(destination_file_name))
          continue
    else:
      logging.info("Files already exists")


def upload_blob(bucket_name, source_file_name, destination_blob_name):
  """
  Uploads a file to the bucket.
  bucket_name = "your-bucket-name"
  The path to your file to upload
  source_file_name = "local/path/to/file"
  The ID of your GCS object
  destination_blob_name = "storage-object-name"
  """

  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)

  blob.upload_from_filename(source_file_name)

  logging.info("File {} uploaded to {}.".format(source_file_name,
                                                destination_blob_name))

# pylint: disable = broad-exception-raised
def download_file_from_gcs(gcs_path, destination_folder_path="data/"):
  """downloads file from gcs"""
  try:
    storage_client = storage.Client()
    bucket_name = gcs_path.split("gs://")[1].split("/")[0]
    bucket = storage_client.get_bucket(bucket_name)
    blob_name = gcs_path.split(bucket_name)[-1].strip("/")
    blob = bucket.blob(blob_name)
    os.makedirs(destination_folder_path, exist_ok=True)
    destination_path = destination_folder_path + blob_name.split("/")[-1]
    blob.download_to_filename(destination_path)
    return destination_path
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise Exception("Failed to download file from the GCS path") from e


def is_valid_path(gcs_path):
  """
    Required format:-
    gcs_uri: gs://bucket-name/prefix/filename.extension
    Returns Boolean value
  """
  storage_client = storage.Client()
  if gcs_path.startswith("gs://") is not True:
    return False
  gcs_uri = gcs_path.strip("/")
  path = gcs_uri.replace("gs://", "").split("/")
  bucket_name = path[0]
  file_path = "/".join(path[1:])
  bucket = storage_client.bucket(bucket_name)
  stats = storage.Blob(bucket=bucket, name=file_path).exists(storage_client)
  return stats


def upload_file_to_bucket(bucket_name, prefix, file_name, file):
  """Upload file to gcs bucket

    Args:
        bucket_name
        prefix: folder name
        file_name: name of file with extension
        file: File to be uploaded

    Returns: uri
    """
  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(f"{prefix}/{file_name}")
  blob.upload_from_file(file, rewind=True)
  return f"gs://{bucket_name}/{prefix}/{file_name}"


def upload_folder(bucket_name, src_path, dest_base_path):
  """Function to upload folder to destination"""
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  for source_file in glob.glob(src_path+"/**",recursive=True):
    # The name of file on GCS once uploaded
    if os.path.isfile(source_file):
      destination_blob_name = dest_base_path+"/"+source_file.replace(
        src_path+"/","")
      blob = bucket.blob(destination_blob_name)
      # The content that will be uploaded
      blob.upload_from_filename(source_file)
      logging.info(
      "File {} uploaded to {}.".format(
      source_file, destination_blob_name
    )
  )


def write_csv_to_bucket(bucket_name, prefix, file_name, file):
  """
  Write a dataframe to a csv file in the gcs bucket
  Args:
    bucket_name
        prefix: folder name
        file_name: name of file with extension
        file: Dataframe to be uploaded
    Returns: uri
  """
  client = storage.Client()
  bucket = client.bucket(bucket_name)
  file_path = f"{prefix}/{file_name}"
  blob = bucket.blob(file_path)
  blob.upload_from_string(file.to_csv(index=False), "text/csv")
  res = f"gs://{bucket_name}/{file_path}"
  return res


def get_blob_from_gcs_path(gcs_path):
  """returns blob object using gcs_path"""
  storage_client = storage.Client()
  bucket_name = gcs_path.split("gs://")[1].split("/")[0]
  blob_name = gcs_path.split(bucket_name)[-1].strip("/")
  bucket = storage_client.bucket(bucket_name)
  if not bucket:
    raise ValueError(f"Unknown path \"{gcs_path}\"")
  blob = bucket.get_blob(blob_name)
  if not blob:
    raise ValueError(f"Unknown path \"{gcs_path}\"")
  return blob

def move_file_within_bucket(bucket_name, src_path, dest_path):
  """
    This function moves a file from src_path to dest_path
    withing the same GCS bucket.
    -------------------------------------------------------
    Input:
      bucket_name `str`: Bucket to upload files
      src_path `str`: Current path of the file on the bucket
      dest_path `str`: Destination path of the file
                        on the bucket
    -------------------------------------------------------
    Output:
      blob_name `str`: Final path of the file on the bucket
    -------------------------------------------------------
    Note:
      if gsutil URI is
        `gs://<bucket_name>/path/to/file/abc.txt`
      then src_path and dest_path should be
        `path/to/file/abc.txt`
  """
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)

  # Remove Bucket name from src_path if it exists
  if src_path[0:len(bucket_name)] == bucket_name:
    src_path = src_path[len(bucket_name):]
  # Remove Bucket name from dest_path if it exists
  if dest_path[0:len(bucket_name)] == bucket_name:
    dest_path = dest_path[len(bucket_name):]

  source_blob = bucket.blob(src_path)
  new_blob = bucket.rename_blob(source_blob, dest_path)
  return new_blob.name

def delete_file_from_gcs(bucket_name, src_path):
  """
    This function deletes a file present at src_path in the
    GCS bucket given by bucket_name
    -------------------------------------------------------
    Input:
      bucket_name `str`: Bucket to upload files
      src_path `str`: Current path of the file on the bucket
    -------------------------------------------------------
    Output:
      File will be deleted
    -------------------------------------------------------
    Note:
      if gsutil URI is
        `gs://<bucket_name>/path/to/file/abc.txt`
      then src_path should be
        `path/to/file/abc.txt`
  """
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)

  # Remove Bucket name from src_path if it exists
  if src_path[0:len(bucket_name)] == bucket_name:
    src_path = src_path[len(bucket_name):]

  blob = bucket.blob(src_path)
  blob.delete()
