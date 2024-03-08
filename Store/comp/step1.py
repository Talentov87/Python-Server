def run(db):
  file_path = "G:/Python/Python-Server/jsons/outputCompanies.json"
  collection_ref = db.collection("COMPANIES")

  # Example: Retrieve documents from the collection
  docs = collection_ref.get()

  docs_list = []

  for doc in docs:
    dat = doc.to_dict()
    dat["id"] = doc.id
    docs_list.append(dat)

  # print(docs_list)
  # Specify the file path where you want to save the JSON file
  import json
  # Write the list of dictionaries to a JSON file
  with open(file_path, "w") as json_file:
      json.dump(docs_list, json_file, indent=4)

  print(f"Documents saved to {file_path}")