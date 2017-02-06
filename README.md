# GoogleCloudStoragePython
read this please
-----------------------------
I think before you can use this file you must install gsutil-standalone version in your computer
https://cloud.google.com/storage/docs/gsutil_install#alt-install


then download json file from Google Cloud Storage
you need configure the .boto file on
	gs_service_key_file = blabla.json <-- your json file

because it work if you did not have the json file to access the service from google cloud service

the bucket name will be look like this = project-[epochtime] to it must be unique for every bucket

--------------------------
-----    script used -----

upload
	python main.py -upload [project_name] [file_name] [file_name] ... + as you need

download
	python main.py -download-bucket [project_name] [bucket_name]

bucket listing
	python main.py -listbucket [project_name]

delete bucket # i setting it on 30 day
	python main.py -cleanup30d [project_name]

-------------------------
-------------------------

please contact me if you need help

	Wisnu Sadewo
