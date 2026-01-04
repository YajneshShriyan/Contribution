import os
import random
import subprocess
import calendar
from datetime import datetime, timedelta


def run_git(args, env=None):
    return subprocess.run(
        ["git"] + args,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )


def get_date(prompt):
    while True:
        value = input(prompt)

        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date. Use YYYY-MM-DD")


# --------------------------------------------------
# Ask for dates
# --------------------------------------------------

start = get_date("Enter start date (YYYY-MM-DD): ")
end = get_date("Enter end date   (YYYY-MM-DD): ")

if start > end:
    print("❌ Start date cannot be after end date.")
    exit(1)


print()
print("📅 Processing:")
print(
    f"   {start.strftime('%Y-%m-%d')} → "
    f"{end.strftime('%Y-%m-%d')}"
)
print()


# --------------------------------------------------
# Create commits
# --------------------------------------------------

current = start
total_commits = 0

monthly_commits = {}
current_month = None
month_total = 0


while current <= end:

    month_key = current.strftime("%Y-%m")

    if current_month is None:
        current_month = month_key

    # If month changed, print previous month
    if month_key != current_month:

        month_name = datetime.strptime(
            current_month,
            "%Y-%m"
        ).strftime("%B %Y")

        print(
            f"✅ {month_name:<15} "
            f"{month_total} commits"
        )

        monthly_commits[current_month] = month_total

        current_month = month_key
        month_total = 0

    # 10-15 commits per day
    commits_today = random.randint(10, 15)

    # Random times during the day
    times = sorted(
        random.randint(0, 86399)
        for _ in range(commits_today)
    )

    for index, seconds in enumerate(times, start=1):

        commit_time = current + timedelta(seconds=seconds)

        date_string = commit_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Make a change
        with open("file.txt", "a") as file:
            file.write(
                f"{date_string}\n"
            )

        run_git(["add", "."])

        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_string
        env["GIT_COMMITTER_DATE"] = date_string

        run_git(
            [
                "commit",
                "-m",
                f"Daily commit {index} "
                f"- {current.strftime('%Y-%m-%d')}"
            ],
            env=env
        )

        total_commits += 1
        month_total += 1

    current += timedelta(days=1)


# Print final month
if current_month:

    month_name = datetime.strptime(
        current_month,
        "%Y-%m"
    ).strftime("%B %Y")

    print(
        f"✅ {month_name:<15} "
        f"{month_total} commits"
    )


# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("=" * 45)
print("🎉 COMPLETED")
print("=" * 45)
print(f"📅 Start date : {start.strftime('%Y-%m-%d')}")
print(f"📅 End date   : {end.strftime('%Y-%m-%d')}")
print(f"📝 Commits    : {total_commits}")
print("=" * 45)


# --------------------------------------------------
# Push
# --------------------------------------------------

push = input("\n🚀 Push to origin/main? (y/n): ")

if push.lower() == "y":

    print("\n🚀 Pushing...")

    run_git(
        ["push", "-u", "origin", "main"]
    )

    print("✅ Push completed!")

else:
    print("⏭️ Push skipped.")

# import os
# from random import randint

# for i in range(1, 4):
#     for j in range(0, randint(1, 10)):
#         d = str(i) + ' days ago\n'
#         with open('file.txt', 'a') as file:
#             file.write(d)
#         os.system('git add .')
#         os.system('git commit --date="01-18-2026" -m "commit "' + str(i) + '"')
       
# os.system('git push -u origin main')