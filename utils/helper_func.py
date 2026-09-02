def admin_filter(
    trainers1,
    fil_by_name=None,
    fil_by_email=None,
    fil_by_skill=None,
    fil_by_status=None
):
    # Initialize with the original DataFrame to guarantee it always exists
    trainers_data = trainers1.copy()

    if fil_by_name:
        trainers_data = trainers_data[trainers_data["name"] == fil_by_name]

    if fil_by_email:
        trainers_data = trainers_data[trainers_data["email"] == fil_by_email]

    if fil_by_skill:
        trainers_data = trainers_data[trainers_data["skill"] == fil_by_skill]

    if fil_by_status:
        trainers_data = trainers_data[trainers_data["status"] == fil_by_status]

    return trainers_data


# Safe integer extraction to prevent NaN ValueErrors
def get_safe_int(val, default_val=0):
    try:
      if pd.isna(val) or str(val).strip() == "":
        return default_val
      return int(float(val))
    except (ValueError, TypeError):
                    return default_val
