import bs4
import numpy as np
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup
from sklearn.linear_model import LinearRegression


# our goal: beginning with just 2017
# ----------------------------------------------------------------
# scrape relevant data from the internet involivng qb rating
# independent of player? (tbd)
# then have machine learn based on amount of touchdowns thrown - x-vec
# y-vec = number of touchdowns
# want to predict # of touchdowns thrown in current week based on offensive
# qb data
# since we want to predict FUTURE touchdown outcomes we will need to
# out the xvec data one week behind the y-vec data
# ----------------------------------------------------------------

# create matrix
xvec = np.ones((488,6))
yvec = np.ones((488,1))

xvec.astype(float)
yvec.astype(float)

link0 = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=2017&year_max=2017&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min=1&week_num_max=16&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat=pass_att&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=pass_rating&from_link=1'
link1 = 'http://pfref.com/tiny/Q1FBt'
link2 = 'http://pfref.com/tiny/wcYG6'
link3 = 'http://pfref.com/tiny/oOox5'
link4 = 'http://pfref.com/tiny/SRMCT'
link5 = 'http://pfref.com/tiny/UQCgn'

# initialize row and column variables
row = 0
col = 0
# ******************************************************************************
#                           ~  begin data scrape ~
# ******************************************************************************
for l in range(0,5):

    if l == 0:
        link = link0
    elif l == 1:
        link = link1
    elif l == 2:
        link = link2
    elif l == 3:
        link = link3
    elif l == 4:
        link = link4
    elif l == 5:
        link = link5
    else:
        print("error in links \n\n\n")

    # scrape data into array here while iterating through
    # weekly links
    client = request(link)
    page_html = client.read()
    client.close()
    page_content = soup(page_html, "html.parser")


    # get all rows
    player_row = page_content.findAll('table')[0].find_all('tr')

    for i in range(len(player_row)):

        # grab relevant data from each row

        row_data = player_row[i].find_all('td')

        if(len(row_data) != 0):
            # make sure we are getting stats for QBs only
            if(row_data[1].text == 'QB'):
                # fill matrix row w data
                cmp_percentage = row_data[14].text
                xvec[row][col] = cmp_percentage
                col+=1

                yds = row_data[15].text
                xvec[row][col] = yds
                col+=1

                tds = row_data[16].text
                # build yvec - tds as a result of qbr & other stats
                yvec[row][0] = tds

                ints = row_data[17].text
                xvec[row][col] = ints
                col+=1

                qbr = row_data[18].text
                xvec[row][col] = qbr
                col+=1

                times_sacked = row_data[19].text
                xvec[row][col] = times_sacked
                col+=1

                #skipped 20 since not relevant
                yds_per_pass = row_data[21].text
                xvec[row][col] = yds_per_pass
                # reset column count to 0 for next row
                col=0
                row+=1
# ******************************************************************************
#                              ~ END data scrape ~
# ******************************************************************************


        # run LogisticRegression
        #-------------------------------------------------------------------
reg = LinearRegression().fit(xvec, yvec)
reg.score(xvec,yvec)

# sample test data
predictx = np.ones((1,6))
predictx[0][0] = 75                 # cmp_percentage
predictx[0][1] = 259                # yards
predictx[0][2] = 0                  # ints
predictx[0][3] = 145                # qbr
predictx[0][4] = 1                  # times_sacked
predictx[0][5] = 11.36            # yds/pass
# then call:
tdprediciton = reg.predict(predictx)

print("Number of estimated touchdowns: " + str(int(tdprediciton)))
