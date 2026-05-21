def load_applications(ParcoursSup project): #In the brackets is name of folder for final code and CSV finles. MUST be the same to run properly!!!
                                            #Anything that says file name must correspond to correct local folder.
 
    applications = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            application = {
                "candidate_id":   int(row["candidate_id"]),
                "program_id":     int(row["program_id"]),
                "score":          int(row["score"]),
                "timestamp":      int(row["timestamp"]),
                "is_scholarship": int(row["is_scholarship"]),
                "hs_id":          int(row["hs_id"])
            }
            applications.append(application)
    return applications

def load_programs(filename):
    
    programs = {}
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs[int(row["program_id"])] = int(row["capacity"])
    return programs


def display_application(app):
    #Sorting of data
    print("--- Application ---")
    print(f"  Candidate ID   : {app['candidate_id']}")
    print(f"  Program ID     : {app['program_id']}")
    print(f"  Score          : {app['score']}")
    print(f"  Timestamp      : {app['timestamp']}")
    print(f"  Scholarship    : {'Yes' if app['is_scholarship'] == 1 else 'No'}")
    print(f"  High School ID : {app['hs_id']}")
    print("-------------------")


def get_applications_by_candidate(applications, candidate_id):
   #Searches for canditate data and returns results.
    results = []
    for app in applications:
        if app["candidate_id"] == candidate_id:
            results.append(app)
    return results

