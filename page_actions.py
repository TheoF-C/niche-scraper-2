ACTIONS = {
    "location":                         [1],
    "acceptance":                       [0, "admissions", "Acceptance Rate"],  # %
    "deadline":                         [0, "admissions", "Application Deadline"],  # Date
    "application fee":                  [0, "admissions", "Application Fee"],  # $
    "sat/act_required":                 [0, "admissions", "SAT/ACT"],
    "gpa_required":                     [0, "admissions", "High School GPA"],
    "early_decision":                   [0, "admissions", "Early Decision/Early Action"],
    "common_app":                       [0, "admissions", "Accepts Common App"],
    "cost":                             [0, "cost", "Net Price"],  # $
    "aid_amount":                       [0, "cost", "Average Total Aid Awarded"],  # $
    "aid_percent":                      [0, "cost", "Students Receiving Financial Aid"],  # %
    "enrollment":                       [0, "students", "Full-Time Enrollment"],
    "part_time_undergrads":             [0, "students", "Part-Time Undergrads"],
    "undergrads_over_25":               [0, "students", "Undergrads Over 25"],  # %
    "pell_grant":                       [0, "students", "Pell Grant"],  # %
    "varsity_athletes":                 [0, "students", "Varsity Athletes"],  # %
    "freshman_on_campus":               [0, "campus-life", "Freshmen Live On-Campus"],  # %
    "median_earnings_after_6_years":    [0, "after", "Median Earnings 6 Years After Graduation"],  # $ / Year
    "graduation_rate":                  [0, "after", "Graduation Rate"],  # %
    "employed_2_years_after":           [0, "after", "Employed 2 Years After Graduation"],  # %
    "popular_majors":                   [2, 3],
    "sat":                              [3, "admissions", "SAT Range"],  # Score Range
    "act":                              [3, "admissions", "ACT Range"],  # Score Range
}
