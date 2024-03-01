from datetime import datetime, timedelta

def generate_hourly_intervals(start_time, end_time):
  """
  Generates hourly intervals between two times, handling special cases.

  Args:
      start_time: A datetime object representing the starting time.
      end_time: A datetime object representing the ending time.

  Returns:
      A list of strings representing the hourly intervals in the format "start_time-end_time".
  """

  # Check if start_time and end_time are datetime objects
  if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
    raise ValueError("start_time and end_time must be datetime objects.")

  # Initialize an empty set to store unique hours
  hours = set()

  # Add all hours between start and end time (inclusive)
  current_hour = start_time.replace(minute=0, second=0, microsecond=0)
  while current_hour <= end_time:
    hours.add(current_hour.strftime('%H:%M:%S'))
    current_hour += timedelta(hours=1)

  # Handle special cases:
  # - If only one "00:00:00" is provided, add the other one for 24 hours.
  if "00:00:00" in hours and len(hours) != 24:
    hours.add("00:00:00")

  # - If only one "12:00:00" is provided, ensure both midday and midnight are included.
  if "12:00:00" in hours and len(hours) != 2:
    hours.add("12:00:00")

  # Convert the set to a sorted list
  intervals = sorted(list(hours))

  return intervals

yesterday = datetime.now() - timedelta(days=1)
start_time = datetime(yesterday.year, yesterday.month, yesterday.day, 18, 0)
end_time = datetime(2024, 3, 1, 10, 0)

intervals = generate_hourly_intervals(start_time, end_time)

print(intervals)