from .time_decode import calculate_submission_time


def make_dict(contestant_data, submission_data, question_ids):
    data = {}
    # contestants_username = contestant_data["username"]
    data["username"] = contestant_data["username"]
    data["rank"] = contestant_data["rank"]
    data["finish_time"] = calculate_submission_time(
        contestant_data["finish_time"])

    if str(question_ids[0]) in submission_data:
        problem_A_st = calculate_submission_time(
            submission_data[str(question_ids[0])]["date"])
        problem_A_flc = submission_data[str(question_ids[0])]["fail_count"]
        data["A_st"] = problem_A_st
        data["A_flc"] = problem_A_flc

    else:
        data["A_st"] = None
        data["A_flc"] = None

    if str(question_ids[1]) in submission_data:
        problem_B_st = calculate_submission_time(
            submission_data[str(question_ids[1])]["date"])
        problem_B_st = submission_data[str(question_ids[1])]["fail_count"]
        data["B_st"] = problem_B_st
        data["B_flc"] = problem_B_st

    else:
        data["B_st"] = None
        data["B_flc"] = None

    if str(question_ids[2]) in submission_data:
        problem_C_st = calculate_submission_time(
            submission_data[str(question_ids[2])]["date"])
        problem_C_flc = submission_data[str(question_ids[2])]["fail_count"]
        data["C_st"] = problem_C_st
        data["C_flc"] = problem_C_flc

    else:
        data["C_st"] = None
        data["C_flc"] = None

    if str(question_ids[3]) in submission_data:
        problem_D_st = calculate_submission_time(
            submission_data[str(question_ids[3])]["date"])
        problem_D_flc = submission_data[str(question_ids[3])]["fail_count"]
        data["D_st"] = problem_D_st
        data["D_flc"] = problem_D_flc

    else:
        data["D_st"] = None
        data["D_flc"] = None

    return data
