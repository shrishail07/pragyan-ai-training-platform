def admin_filter(
    trainers,
    fil_by_name = None,
    fil_by_email = None,
    fil_by_skill = None
):

    if fil_by_name:
        trainers_data = trainers_data[
            trainers_data["name"] == fil_by_name
        ]

    if fil_by_email:
        trainers_data = trainers_data[
            trainers_data["email"] == fil_by_email
        ]

    if fil_by_skill:
        trainers_data = trainers_data[
            trainers_data["skill"] == fil_by_skill
        ]

    return trainers_data
