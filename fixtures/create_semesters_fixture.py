import pendulum


def get_semester_name(date: pendulum.datetime) -> str:
    first_semester_start_month = 9
    second_semester_start_month = 3
    school_semester = 'I'
    if date.month >= first_semester_start_month:
        school_year = str(date.year) + '/' + str("%02d" % ((date.year + 1) % 100))
    else:
        school_year = str(date.year - 1) + '/' + str("%02d" % (date.year % 100))
        if date.month >= second_semester_start_month:
            school_semester = 'II'
    return school_year + " " + school_semester


date = pendulum.date(2020, 10, 1)

print('[')
for i in range(100):
    print('{')
    print('\t"model": "teacher.semester",')
    print(f'\t"pk": {i + 1},')
    print('\t"fields": {')
    print(f'\t\t"name": "{get_semester_name(date)}"')
    date = date.add(months=6)
    print('\t}')
    print('},')

# w pliku końcowym usunąć przecinek po statnim rekordzie
print(']')
