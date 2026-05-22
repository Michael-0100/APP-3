

# ===(FULL CODE BELOW)===

import csv
import time


# Importation of data from csv files aand sorted into dictionaries and lists
def load_applications(Files_vs):
    
    applications = []
    with open(Files_vs, newline='', encoding='utf-8') as f:
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


def load_programs(Files_vs): # Function which reads the program data and returns a dictionary linking program_id to capacity.
    
    programs = {}
    with open(Files_vs, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs[int(row["program_id"])] = int(row["capacity"])
    return programs


#Data formatting 

def display_application(app):

    print("--- Application ---")
    print(f"  Candidate ID   : {app['candidate_id']}")
    print(f"  Program ID     : {app['program_id']}")
    print(f"  Score          : {app['score']}")
    print(f"  Timestamp      : {app['timestamp']}")
    print(f"  Scholarship    : {'Yes' if app['is_scholarship'] == 1 else 'No'}")
    print(f"  High School ID : {app['hs_id']}")
    print("----")


def get_applications_by_candidate(applications, candidate_id): #Gives all the applications for a given candidate_id. 
  
    results = []
    for app in applications:
        if app["candidate_id"] == candidate_id:
            results.append(app)
    return results


def group_by_program(applications): #Organises the applications by program_id and returns a dict with list of applications for each program_id.
    
    grouped = {}
    for app in applications:
        pid = app["program_id"]
        if pid not in grouped:
            grouped[pid] = []
        grouped[pid].append(app)
    return grouped


#Sorting algorithms

# Insertion Sort 
def insertion_sort(lst, key_func): #Sorts list in place using insertion sort. key_func is a function that extracts the value to compare from each item. Sorts in descending order (highest score first).
    
    for i in range(1, len(lst)):
        current = lst[i]
        j = i - 1
        while j >= 0 and key_func(lst[j]) < key_func(current):
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = current
    return lst


# --- Merge Sort #returns a new sorted list using merge sort (Again in descending order)
def merge_sort(lst, key_func):
   
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left  = merge_sort(lst[:mid], key_func)
    right = merge_sort(lst[mid:], key_func)
    return merge(left, right, key_func)


def merge(left, right, key_func): #Merges two sorted lists in descending order.

    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) >= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Quicksort 
def quicksort(lst, key_func): #Returns a new sorted list using quicksort (descending).
    
    if len(lst) <= 1:
        return lst

    pivot = lst[len(lst) // 2]
    pivot_val = key_func(pivot)

    left   = [x for x in lst if key_func(x) > pivot_val]
    middle = [x for x in lst if key_func(x) == pivot_val]
    right  = [x for x in lst if key_func(x) < pivot_val]

    return quicksort(left, key_func) + middle + quicksort(right, key_func)


# Bucket Sort 
def bucket_sort_by_score(lst): # """ Sorts applications by score using bucket sort. Works because scores are bounded integers (0..10000). Returns a new list sorted in DESCENDING order by score.

    if not lst:
        return []

    MAX_SCORE = 10001
    buckets = [[] for _ in range(MAX_SCORE)]

    for app in lst:
        buckets[app["score"]].append(app)

    result = []
    for score in range(MAX_SCORE - 1, -1, -1):
        result.extend(buckets[score])

    return result


#Ranking policies

def policy_baseline(applications_for_program): #Policy 1 - Baseline
    """
    Sort by exam scores in descending order.
    Ties broken by times of application (First applications given priority).
    Final tie-break: candidate_id (Higher candidate_ids win) (Returns the same result each time & verifiable).
    What is the flaw here? -> tiny score differences can create micro-gaps that separate candidates unfairly, (Candidate should be ranked first if 99.5 or 99 vs 100 etc.)
     scholarship students may end up last if scores are tied
    """
    def sort_key(app):
        return (-app["score"], app["timestamp"], app["candidate_id"])

    return sorted(applications_for_program, key=sort_key)


def policy_corrected(applications_for_program): #Policy 2 - (fairer + more auditable)
    """

    Fixes from policy 1:
      1. Micro-gaps: All exam are scores rounded to the nearest 100 points, creating score bands (e.g. 900-999, 800-899, etc.) that group candidates together,
         so tiny differences don't unfairly separate candidates.
      2. For tie breaks, scholarship students take priority if they are withing the same score band. (Done to address fairness)
         
   Second tie-break is the timestamp, then candidate_id.
    """
    def sort_key(app):
        band = (app["score"] // 100) * 100
        scholarship_priority = 0 if app["is_scholarship"] == 1 else 1
        return (-band, scholarship_priority, app["timestamp"], app["candidate_id"])

    return sorted(applications_for_program, key=sort_key)


# ParcoursSup program 

def compute_call_order(applications, programs, policy="corrected"): 
    """
    For each course, it ranks its applicants and splits them into:
      - accepted: Highest ranked candidates up to the program's capacity, everyone else goes to the waiting list. 
      Waiting list is ordered by the same ranking.
    """
    grouped = group_by_program(applications)
    results = {}

    for pid, apps in grouped.items():
        if policy == "baseline":
            ranked = policy_baseline(apps)
        else:
            ranked = policy_corrected(apps)

        capacity     = programs.get(pid, 0)
        accepted     = ranked[:capacity]
        waiting_list = ranked[capacity:]

        results[pid] = {
            "ranked":       ranked,
            "accepted":     accepted,
            "waiting_list": waiting_list
        }

    return results


def display_program_results(results, program_id, max_show=10):
    """Prints  results for one program."""
    if program_id not in results:
        print(f"Program {program_id} not found.")
        return

    data         = results[program_id]
    accepted     = data["accepted"]
    waiting_list = data["waiting_list"]

    print(f"\n=== Program {program_id} ===")
    print(f"  Capacity    : {len(accepted)}")
    print(f"  Waiting list: {len(waiting_list)}")

    print(f"\n   Accepted (top {min(max_show, len(accepted))}) ")
    for i, app in enumerate(accepted[:max_show]):
        print(f"{i+1:3}. Candidate {app['candidate_id']:6} "
              f"Score={app['score']}  "
              f"Scholarship={'Y' if app['is_scholarship'] else 'N'} "
              f"HS={app['hs_id']}")

    print(f"\n   Waiting list (top {min(max_show, len(waiting_list))})")
    for i, app in enumerate(waiting_list[:max_show]):
        print(f"  {i+1:3}. Candidate {app['candidate_id']:6}  "
              f"Score={app['score']}  "
              f"Scholarship={'Y' if app['is_scholarship'] else 'N'}")


# Audit tests

def audit_arbitrary_ties(applications, program_id=1):
    """
    AUDIT 1:
    Looks for candidates with the same exact score in a program.
    Shows how the two policies handle them differently.
    """
    print("\n AUDIT: 1 - Ties with same score ")
    apps = [a for a in applications if a["program_id"] == program_id]

    score_count = {}
    for app in apps:
        s = app["score"]
        score_count[s] = score_count.get(s, 0) + 1

    ties = {s: c for s, c in score_count.items() if c > 1}
    print(f"Program {program_id}: {len(apps)} applicants, "
          f"{len(ties)} score values shared by multiple candidates.")

    if ties:
        worst_score = max(ties, key=lambda s: ties[s])
        tied_apps   = [a for a in apps if a["score"] == worst_score]
        print(f"\n  Worst tie: score={worst_score}, {ties[worst_score]} candidates.")

        print("\n  Baseline order (timestamp tie-break, scholarship may end up last):")
        for app in policy_baseline(tied_apps):
            print(f"    Candidate {app['candidate_id']}  "
                  f"ts={app['timestamp']}  "
                  f"scholarship={'Y' if app['is_scholarship'] else 'N'}")

        print("\n  Corrected order (scholarship priority + score band):")
        for app in policy_corrected(tied_apps):
            print(f"    Candidate {app['candidate_id']}  "
                  f"ts={app['timestamp']}  "
                  f"scholarship={'Y' if app['is_scholarship'] else 'N'}")


def audit_microgaps(applications, program_id=1):
    """
    AUDIT 2: Micro-gaps
    Shows how many candidates are separated by less than 100 points
    and how many positions change between the two policies.
    """
    print("\n AUDIT: Micro-gaps ")
    apps             = [a for a in applications if a["program_id"] == program_id]
    ranked_baseline  = policy_baseline(apps)
    ranked_corrected = policy_corrected(apps)

    reversals = 0
    for i in range(len(ranked_baseline)):
        if ranked_baseline[i]["candidate_id"] != ranked_corrected[i]["candidate_id"]:
            reversals += 1

    total = len(apps)
    print(f"Program {program_id}: {total} applicants.")
    print(f"  Positions changed between baseline and corrected: {reversals} "
          f"({100*reversals//total if total > 0 else 0}% of candidates)")

    micro_gaps = 0
    for i in range(len(ranked_baseline) - 1):
        diff = ranked_baseline[i]["score"] - ranked_baseline[i+1]["score"]
        if 0 < diff < 100:
            micro_gaps += 1

    print(f"  Adjacent pairs separated by < 100 points: {micro_gaps}")
    print("  These micro-gaps are eliminated in the corrected policy.")


# Performance audit

def audit_performance():
    """
    AUDIT 3 
    Compares insertion sort (O(n²)) to merge sort (O(n log n))
    across all three dataset sizes to prove insertion is impractical.
    """
    print("\n AUDIT: Performance across all datasets")

    datasets = [
        ("parcoursup_small_10000.csv",   "small   (10,000)"),
        ("parcoursup_medium_100000.csv",  "medium  (100,000)"),
        ("parcoursup_massive_500000.csv", "massive (500,000)"),
    ]

    print(f"\n  Merge sort — full dataset timing:")
    print(f"  {'Dataset':<22}  {'Records':>8}  {'Time':>10}")
    print("  " + "-" * 45)

    for filename, label in datasets:
        print(f"  Loading {label}...", end=" ", flush=True)
        apps = load_applications(filename)
        t0   = time.time()
        merge_sort(apps[:], key_func=lambda a: a["score"])
        t    = time.time() - t0
        print(f"{len(apps):>8} records  {t:.4f}s")

    print("\n  Insertion vs merge sort on small dataset (n up to 5000):")
    small_apps = load_applications("parcoursup_small_10000.csv")
    print(f"  {'n':>6}  {'insertion':>12}  {'merge':>10}  {'ratio':>8}")
    print("  " + "-" * 42)

    for n in [500, 1000, 2000, 5000]:
        sample = small_apps[:n]

        t0  = time.time()
        insertion_sort(sample[:], key_func=lambda a: a["score"])
        t_ins = time.time() - t0

        t0  = time.time()
        merge_sort(sample[:], key_func=lambda a: a["score"])
        t_mrg = time.time() - t0

        ratio = (t_ins / t_mrg) if t_mrg > 0 else float('inf')
        print(f"  {n:>6}  {t_ins:>11.4f}s  {t_mrg:>9.4f}s  {ratio:>7.1f}x")

    print("\n  An O(n^2) sort would be completely impractical at 500,000 records.")


#Comparison of all algorithms on small dataset 

def benchmark_algorithms(applications):
    """
    Compares insertion sort, merge sort, quicksort, and bucket sort
    on different dataset sizes and prints a comparison table.
    """
    print("\n BENCHMARK: All Sorting Algorithms ")
    print(f"{'n':>8}  {'insertion':>12}  {'merge':>10}  "
          f"{'quick':>10}  {'bucket':>10}")
    print("-" * 58)

    sizes = [500, 1000, 2000, 5000, 10000]

    for n in sizes:
        sample = applications[:n]

        if n <= 5000:
            t0    = time.time()
            insertion_sort(sample[:], key_func=lambda a: a["score"])
            t_ins = time.time() - t0
            ins_str = f"{t_ins:.4f}s"
        else:
            ins_str = "  (skipped)"

        t0      = time.time()
        merge_sort(sample, key_func=lambda a: a["score"])
        t_merge = time.time() - t0

        t0      = time.time()
        quicksort(sample, key_func=lambda a: a["score"])
        t_quick = time.time() - t0

        t0       = time.time()
        bucket_sort_by_score(sample)
        t_bucket = time.time() - t0

        print(f"{n:>8}  {ins_str:>12}  {t_merge:>9.4f}s  "
              f"{t_quick:>9.4f}s  {t_bucket:>9.4f}s")


# Main function to run the prototype and audits

def main():
    print("=" * 60)
    print("  ParcoursSup Code runthrough and audits")
    

    # All three dataset pairs
    datasets = [
        ("parcoursup_small_10000.csv",   "parcoursup_programs_small_800.csv",    "SMALL   (10,000)"),
        ("parcoursup_medium_100000.csv",  "parcoursup_programs_medium_2500.csv",  "MEDIUM  (100,000)"),
        ("parcoursup_massive_500000.csv", "parcoursup_programs_massive_5000.csv", "MASSIVE (500,000)"),
    ]

    for apps_file, programs_file, label in datasets:
        print(f"\n{'='*60}")
        print(f"  Dataset: {label}")
        print(f"{'='*60}")

        # 1. Load data
        print(f"\n[1] Loading data...")
        applications = load_applications(apps_file)
        programs     = load_programs(programs_file)
        print(f"  Loaded {len(applications)} applications.")
        print(f"  Loaded {len(programs)} programs.")

        # 2. Display a sample + find a candidate
        print("\n[2] Sample application (first record):")
        display_application(applications[0])

        example_id     = applications[0]["candidate_id"]
        candidate_apps = get_applications_by_candidate(applications, example_id)
        print(f"\n  Candidate {example_id} has {len(candidate_apps)} application(s):")
        for a in candidate_apps:
            print(f"    -> Program {a['program_id']}, score={a['score']}")

        # 3. Sort program 1 and show top 5
        print("\n[3] Sorting applicants for program 1 (merge sort):")
        prog1_apps   = [a for a in applications if a["program_id"] == 1]
        sorted_prog1 = merge_sort(prog1_apps, key_func=lambda a: a["score"])
        print(f"  Program 1 has {len(sorted_prog1)} applicants. Top 5:")
        for i, app in enumerate(sorted_prog1[:5]):
            print(f"    {i+1}. Candidate {app['candidate_id']}  score={app['score']}")

        # 4. Compute call orders with both policies
        print("\n[4 & 5] Computing call orders with both policies...")
        results_baseline  = compute_call_order(applications, programs, policy="baseline")
        results_corrected = compute_call_order(applications, programs, policy="corrected")

        print("\n  -- BASELINE --")
        display_program_results(results_baseline, program_id=1)

        print("\n  -- CORRECTED --")
        display_program_results(results_corrected, program_id=1)

        # 7. Audit tests on this dataset
        print("\n[7] Audit tests...")
        audit_arbitrary_ties(applications, program_id=1)
        audit_microgaps(applications, program_id=1)

    # 6. Performance audit loads all datasets itself
    audit_performance()

    # Bonus benchmark on small dataset (insertion would be too slow on larger)
    print("\n[Benchmark] All four algorithms on small dataset:")
    small_apps = load_applications("parcoursup_small_10000.csv")
    benchmark_algorithms(small_apps)

    print("\n[Done] Prototype finished.")


if __name__ == "__main__":
    main()
