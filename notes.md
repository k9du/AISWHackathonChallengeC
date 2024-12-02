+ Each file takes 10 secs to create metadata for. Whats the total time taken to create metadata for all the files? Too long. Save to db? I don't know.
+ OpenAI api doesn't support every file extension e.g., .laz isn't allowed and there are lots of them in the test set. Potential issue?
+ allowed_extensions = ["c", "cpp", "css", "csv", "doc", "docx", "gif", "go", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", "php", "pkl", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"]
