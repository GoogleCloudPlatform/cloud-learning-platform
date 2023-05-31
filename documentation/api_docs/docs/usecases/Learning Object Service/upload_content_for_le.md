---
sidebar_label: Upload Content for LE
sidebar_position: 6
---

# Upload Content at Learning Experience and link it to child Learning Resource

The following steps are to upload and link content to the Learning Experience and underlying child Learning Resource. Depending on the type of content you wish to link, the behaviour of the API will differ. 

### Two Scenarios of Content Upload at Learning Experience
1. Upload a Generic Madcap Zip
2. Upload a SRL Madcap Zip

#### 1. What is a Generic Madcap Zip ?
A general Madcap zip is any valid Madcap zip file that follows the following rules
1. It contains a file named `Default.htm`
2. It contains a folder named `Content`
3. There is atleast one `.htm` file in the `Content` folder

#### 2. What is an SRL Madcap Zip ?
SRL Madcap zip is a valid Madcap Zip that satisfies the above given conditions, along with a few more specific to SRLs
1. The name of the zip starts with `SRL`. eg: `SRL_sample_1.zip`
2. The names of the `.htm` files in the `Content` folder also start with `SRL`. eg: `SRL_module_1.htm`
3. There is atleast one `SRL_<some_name>.htm` file in the `Content` folder

#### 3. How does the behaviour of the APIs differ for SRL upload ?

1. The SRL madcap export once uploaded against any given Learning Experience, will be automatically made available for other Learning Experiences for the same Program. Thus we can say, an SRL madcap export holds SRL modules for multiple Learning Experiences.

Assume the following hierarchy structure.

```
    Pathway
        |
        + Learning Experience 1 <- Upload SRL Here
            |
            + SRL Module 1
            + SRL Module 2
        + Learning Experience 2 <- Automatically Access SRL Here
            |
            + SRL Module 3

```

As described in the above snippet, if you upload a valid SRL madcap export against Learning Experience 1, then it will also be linked to the sibling LE, i.e Learning Experience 2. Which implies, that the child SRL Modules and the underlying Learning Resources can be linked to any `.htm` file of the linked SRL. Upload Once, use every where!


2. A generic madcap export once uploaded against any given Learning Expereince will only be available for the child nodes of the Learning Experience. Thus we can say, a general Madcap export holds resource content for a single Learning Experience.

Assume the following hierarchy structure.

```
    Pathway
        |
        + Learning Experience 1 <- Upload Madcap export here
            |
            + Module 1
                |
                + Resource 1
                + Resource 2
            + Module 2
                |
                + Resource 3
        + Learning Experience 2 <- Upload another Madcap export here
            |
            + Module 3
                |
                + Resource 4

```
In the above given scenario, the content once uploaded against a given Learning Experience will only be made available to its child nodes. Thus a madcap export uploaded for Learning Experience will only be linkable for Resource 1, Resource 2 and Resource 3

If you try to link some valid content file for the Learning Experience 2, then this action is forbidden, because the link was not made against the parent Learning Experience.

#### 4. How can I identify which file can be linked to a Learning Resource?
1. You need to check the `resource_path` field of the parent Learning Experience, or the `srl_resource_path` field in case we wish to link a SRL.
2. If the `resource_path` is something like, `learning-resources/Folder_ABC` , then the child learning resource can only be linked to a file that belongs to the folder `Folder_ABC`. Same applies for `srl_resource_path` field of the LE.


#### 5. What does a valid Madcap Export look like?
A Madcap export recognised by the Learning Object Service is a zip file that contains:
1. A ```Default.htm``` file as the entrypoint to the package.
2. A folder named ```Content``` which hold multiple linkable ```.htm``` files.
3. A valid Madcap export must have atleast one linkable ```.htm``` file in the ```Content``` folder.
4. ```Content``` folder which can have multiple nested folders with their own children ```.htm``` files. These nested files will be counted towards the total linkable ```.htm``` file count in the ```Content``` folder.
5. An exception to above point is that the ```.htm``` files present in the following list of folders will not be counted toward total linkable html files. ```["Resources", "Templates"]```

```
  Sample_Madcap_Export.zip
    |
    + Default.htm
    + Content
        |
        + Folder A
            |
            + def.htm
        + abc.htm

```

There can be any other files like ```.js```, ```.css```, or assets in the uploaded zip, they are essential, but will not be used as far as linking the content to the hierarchy is concerned. Hence these files will be ignored for validation by LOS. Albeit, these files should be present in the zip file to ensure the content is rendered correctly.

Thus, a generic madcap export would look like this:

```
  Sample_Madcap_Export.zip
    |
    + Default.htm
    + Default.js
    + Data
    + Resources
    + Skins
    + Content
        |
        + Resources
        + Templates
        + Folder_A
            |
            + def.htm
        + abc.htm

```

In the above example, only abc.htm and Folder_A.htm are linkable html files, hence total linkable ```.htm``` files is 2 even if other ```.htm``` files could be present inside ```Content``` folder.

#### Points to remember while uploading content against LE
If a madcap export is already linked to the LE, and we want to update it, then 3 scenarios will be encountered.
1. If new zip file has same name and internal html file names map 1:1 with the export which is currently linked:
    In this case, the existing contents will be overriden and the existing links will be automatically updated.
2. If new zip file has a different name but internal html file names map 1:1 with the export which is currently linked:
    In this case, a new folder will be created on GCS bucket for new contents and the existing links will be automatically updated.
3. If the contents of the new zip file do not map 1:1 with the exisiting export, that means some (or all) files are missing. In that case, the server will respond with the list of the missing files.


With this information, we can now proceed to use the endpoints for uploading content against a Learning Experience.

### Step 1: Ensure we have a Learning Hierarchy

Ideally the hierarchy should be ingested from the bulk import APIs and it should follow the general structure

```
Pathway - Program
    |
    + Pathway - Level
        |
        + Pathway - Descipline
            |
            + Pathway - Unit 1
                |
                + Learning Experience 1
                    |
                    + Learning Object 1
                        |
                        + Learning Object 2
                            |
                            + Learing Resource 1
                            + Learing Resource 2
                        + Learing Resource 3
                        + Learing Resource 4
                    + Learing Object 3
                        |
                        + Learning Resource 5
``` 
    
> **Note**
>
> As described in above example, a Learning Object may have children as Learning Objects and Learning Resource at the same time. 
> Although, LR1, LR2 are children of LO2, they are indirectly the children of LO1 and LE2. Similarly for LR3,LR4 and LR5, they all will be considered as the child Learning Resources of the Learning Experience 1.

### Step 2: Upload Madcap Export

By default there will be no content linked to the learning experience, hence the ```resource_path``` and `srl_resource_path` field of the learning experience will be empty. To upload madcap export use the following endpoint.

**POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/content-serving/upload/madcap/{le_uuid}`**.

Parameters to be sent with the request are:

1. `le_uuid`: The learning experience against which the content should be uploaded

2. `content_file`: The content zip file should be a Binary File

3. `is_srl`: This boolean flag determines the behaviour of the endpoint. If set to `true`, the `srl_resource_path` field of the LE will be updated otherwise `resource_path`.

When a new content is uploaded it will be stored on the GCS bucket then the prefix of the location where the file is stored will be returned in the madcap export format. which means it will only return the list of ```.htm``` files which are present in the ```Content``` folder of the Madcap export

The response will look like:

```json
    {
  "success": true,
  "message": "Successfully uploaded the content for learning experience with uuid 3kViCH02kOycjwsSjjc0",
  "data": {
    "prefix": "learning-resources/Sample_Madcap_Export_v2/",
    "files": [
      "learning-resources/Sample_Madcap_Export_v2/Test Output/Content/ENG23516-M1-1-unitoverview.htm",
      "learning-resources/Sample_Madcap_Export_v2/Test Output/Content/ENG23516-M2-1-moduleoverview.htm",
      ...],
    "folders": []
  }
}

```

At this point, if you fetch the Learning Experience by UUID, it will show that the `resource_path` or `srl_resource_path` of the LE is populated based on the selected option. This will act as a validator for the link created between child Learning Resources and GCS contents.

> **Warning**
> Currently the maximum allowed file size is set to 200MB.




### Step 3: List contents from GCS bucket in Madcap format

The Madcap ```.htm``` present in the ```Content``` folder will can listed using the following endpoint.
`<APP_URL>/learning-object-service/api/v1/content-serving/list-contents`

Query Params:

```prefix``` : the prefix for which the contents should be listed

```list_madcap_contents``` : set ```true``` if the content is expected in madcap format

> **Note**
>
> To create a dropdown of madcap specific files, use the ```list_madcap_contents``` flag. default is false.
> To list contents present in any folder in gcs bucket, do not pass this query param.

If the learning resource is valid, then you will receive a json response as below.


#### When response is required in Madcap format
```json
{
  "success": true,
  "message": "Successfully listed all files and folder at given prefix",
  "data": {
    "prefix": "learning-resources/Sample_Madcap_Export_v2/",
    "files": [
      "learning-resources/Sample_Madcap_Export_v2/Test Output/Content/ENG23516-M1-1-unitoverview.htm",
      "learning-resources/Sample_Madcap_Export_v2/Test Output/Content/ENG23516-M2-1-moduleoverview.htm",
      ...
    ],
    "folders": []
  }
}
```
#### Otherwise
```json
{
  "success": true,
  "message": "Successfully listed all files and folder at given prefix",
  "data": {
    "prefix": "learning-resources/",
    "files": [
      "learning-resources/test.html",
      "learning-resources/video.mp4"
    ],
    "folders": [
      "learning-resources/Docx Rendering",
      "learning-resources/NS_HUM102_C1_S2_Academic Programs of the Humanities_SCORM1.2",
      "learning-resources/RuntimeBasicCalls_SCORM20043rdEdition",
      "learning-resources/Sample_FAQ",
      "learning-resources/Sample_Madcap_Export",
      ...
    ]
  }
}
```

### Step 4: Link Content to Learning Resource

To link content to a learning resource, ensure it is a valid child of the learning experience. A learning resource will only be allowed to link a resource path if the path contains the prefix specified by the parent learning experience. 

eg:
If the learning experience has a ```resource_path``` : ```learning-resources/Sample_Madcap_Export_v2/```

Then the learning resource must have the same prefix. hence a valid linkable path should look like ```learning-resources/Sample_Madcap_Export_v2/Test Output/Content/ENG23516-M1-1-unitoverview.htm```

Make a POST api call to `<APP_URL>/learning-object-service/api/v1/content-serving/link/madcap/{le_uuid}/{lr_uuid}`

Params:

1. ```le_uuid``` : the unique id of the learning experience for which content was uploaded in step 2 
2. ```lr_uuid```: the unique id of the learning resource which is the child of the learning experience ```le_uuid``` and for which the path should be linked.
3. ```is_srl```: this boolean flag determines if the content is of type SRL. 

Request Body:

```json
{
  "resource_path": "learning-resources/Sample_Madcap_Export_v2/Test Output/Content/ENG23516-M1-1-unitoverview.htm",
  "type": "html"
}
```

If the le_uuid, lr_uuid and the resource_path is valid, then you will receive a json response as below.

```json
{
  "success": true,
  "message": "Successfully linked content to Learning Resource with uuid {lr_uuid}"
}
```

At this point, the resource_path and type field of the learning resource will be populated as specified in the request body.


### Step 5: Generate Signed URL

To generate a signed url, the content should be linked to a learning resource.Make a GET api call to **`<APP_URL>/learning-object-service/api/v1/content-serving/{uuid}`**

```uuid``` : the unique id assigned to the learning resource

If the learning resource is valid and has a linked content, then you will receive a json response as below.

```json
{
  "success": true,
  "message": "Successfully fetched the signed url",
  "data": {
    "signed_url": "http://some/signed_url",
    "resource_type": "html",
    "resource_uuid": "lr_uuid"
  }
}
```