from MySQLdb import connect, IntegrityError
from csv import DictReader


def main():
    insert_company_string = 'INSERT INTO Company (title, website, ceo, employees, sector_ID, industry_ID, ceo_title_ID) \
                              VALUES (%s, %s, %s, %s, %s, %s, %s);'
    insert_hq_string = 'INSERT INTO HQ (company_ID, street, city, hq_state, zip, phone) \
                        VALUES (%s, %s, %s, %s, %s, %s);'
    insert_alias_string = 'INSERT INTO Alias (company_ID, ticker, full_name) VALUES (%s, %s, %s);'
    insert_sector_string = 'INSERT INTO Sector (sector) VALUES (%s);'
    insert_industry_string = 'INSERT INTO Industry (industry) VALUES (%s);'
    insert_ceo_title_string = 'INSERT INTO CeoTitle (title) VALUES (%s);'
    insert_year_rank_string = 'INSERT INTO YearRank (company_ID, year, ranking, revenues, profits, assets)\
                                VALUES (%s, %s, %s, %s, %s, %s);'

    conn = connect(host="localhost", user="root",
                   passwd="Alpha2018", db="companyDB")
    c = conn.cursor()

    # this isn't technically necessary with our data, but it's a good idea
    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    with open('raw_data.csv', encoding="utf8") as mfile:
        reader = DictReader(mfile)
        for row in reader:
            sector_id = doSector(c, insert_sector_string, row)
            industry_id = doIndustry(c, insert_industry_string, row)
            ceo_title_id = doCeoTitle(c, insert_ceo_title_string, row)
            company_id = doCompany(
                c, insert_company_string, row, sector_id, industry_id, ceo_title_id)
            doHQ(c, insert_hq_string, row, company_id)
            doAlias(c, insert_alias_string, row, company_id)
            doYearRank(c, insert_year_rank_string, row, company_id)
    conn.commit()
    conn.close()


def doSector(cursor, insert_string, row):
    try:
        cursor.execute(insert_string, [row['Sector']])
        sector_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute(
            'SELECT sector_ID FROM Sector WHERE sector = %s;', [row['Sector']])
        sector_id = cursor.fetchone()[0]
    return sector_id


def doIndustry(cursor, insert_string, row):
    try:
        cursor.execute(insert_string, [row['Industry']])
        industry_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute('SELECT industry_ID FROM Industry WHERE industry = %s;', [
                       row['Industry']])
        industry_id = cursor.fetchone()[0]
    return industry_id


def doCeoTitle(cursor, insert_string, row):
    try:
        cursor.execute(insert_string, [row['Ceo-title']])
        ceo_title_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute('SELECT ceo_title_ID FROM CeoTitle WHERE title = %s;', [
                       row['Ceo-title']])
        ceo_title_id = cursor.fetchone()[0]
    return ceo_title_id


def doCompany(cursor, insert_string, row, sector_id, industry_id, ceo_title_id):
    try:
        cursor.execute(insert_string, [row['Title'], row['Website'], row['Ceo'],
                                       row['Employees'], sector_id, industry_id, ceo_title_id])
        company_id = cursor.lastrowid
    except IntegrityError:
        cursor.execute(
            'SELECT company_ID FROM Company WHERE title = %s;', [row['Title']])
        company_id = cursor.fetchone()[0]
    return company_id


def doHQ(cursor, insert_string, row, company_id):
    try:
        cursor.execute(insert_string, [
                       company_id, row['Hqaddr'], row['Hqcity'], row['Hqstate'], row['Hqzip'], row['Hqtel']])
    except IntegrityError:
        pass


def doAlias(cursor, insert_string, row, company_id):
    try:
        cursor.execute(insert_string, [
                       company_id, row['Ticker'], row['Fullname']])
    except IntegrityError:
        cursor.execute(
            'SELECT full_name FROM Alias WHERE company_ID = %s;', [company_id])
        current_full = cursor.fetchone()[0]
        if len(row['Fullname']) > len(current_full):
            cursor.execute('UPDATE Alias SET full_name = %s WHERE company_ID = %s;', [
                           row['Fullname'], company_id])


def doYearRank(cursor, insert_string, row, company_id):
    cursor.execute(insert_string, [
                   company_id, row['Year'], row['Rank'], row['Revenues'], row['Profits'], row['Assets']])


main()
