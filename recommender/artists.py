'''
Created on 21.07.2013
@author: Marius Kaminskas

A class containing the dictionary with artist information:
{gid : 
    {"artistName" : <artist name>,
     "lfTags" : [<list of tags>],
     "lfSimilar" : [<list of similar artist gids>],
     "genres" : [<list of genres>],
     "fanCountries" : [<list of country codes>],
     "fanCities" : [<list of cities>],
     "fanGender" : <'male'/'female'>,
     "fanAge" : [<list of age values>],
     "fans" : [<list of userIDs>]} }
'''

import fileIO
import json

class Artists:
    
    def __init__(self):
        self.artists = {}
        
    def printToFile(self):
        data = []
        for gid, artistInfo in self.artists.iteritems():
            data.append([gid,json.dumps(artistInfo)])
        fileIO.writeCSVFile('outputData/artist_info.csv', ['gid','info_json'], data)
    
    # add all artists that have a gid and a name
    def addArtistNames(self):
        for artistEntry in fileIO.readCSVFile('trainingData/sm_artist.csv'):
            name = artistEntry[1]
            gid = artistEntry[2]
            if ((gid not in self.artists) and (gid != 'N')):
                self.artists[gid] = {'artistName':name}
        for artistEntry in fileIO.readCSVFile('trainingData/lf_artist_similar.csv'):
            name = artistEntry[2]
            gid = artistEntry[1]
            if ((gid not in self.artists) and (gid != 'N')):
                self.artists[gid] = {'artistName':name}
        for artistEntry in fileIO.readCSVFile('trainingData/dz_artist.csv'):
            name = artistEntry[3]
            gid = artistEntry[2]
            if ((gid not in self.artists) and (gid != 'N')):
                self.artists[gid] = {'artistName':name}
                
    # get Last.fm tags for all artists
    def addArtistLastFmTags(self):
        for dataEntry in fileIO.readCSVFile('trainingData/lf_artist_tag.csv'):
            gid = dataEntry[1]
            if (gid in self.artists):
                jsonTags = json.loads(dataEntry[2])
                tags = []
                for tagEntry in jsonTags:
                    if (tagEntry['tag']):
                        tags.append(tagEntry['tag'])
                if(tags):
                    artistData = self.artists[gid]
                    artistData['lfTags'] = tags
                    self.artists[gid] = artistData
    
    # get similar artist IDs from Last.fm dataset
    def addSimilarArtists(self):
        for dataEntry in fileIO.readCSVFile('trainingData/lf_artist_similar.csv'):
            gid = dataEntry[1]
            gidSimilar = dataEntry[3]
            if ((gid in self.artists) and (gidSimilar != '0') and (gid != gidSimilar)):   
                artistData = self.artists[gid]
                if ('lfSimilar' not in artistData):
                    artistData['lfSimilar'] = [gidSimilar]
                elif (gidSimilar not in artistData['lfSimilar']):
                    artistData['lfSimilar'].append(gidSimilar)
                self.artists[gid] = artistData
    
    # get the genre labels of artist releases (from Deezer dataset) 
    def addArtistGenres(self):
        for dataEntry in fileIO.readCSVFile('trainingData/dz_artist.csv'):
            dz_id = dataEntry[0]
            gid = dataEntry[2]
            if (gid in self.artists):
                releases = fileIO.getCSVRowsByFieldValue('trainingData/dz_release.csv', 'dz_artist_id', dz_id)
                if (releases):
                    genres = []
                    for releaseEntry in releases:
                        genreId = releaseEntry[4]
                        genreEntry = fileIO.getCSVRowsByFieldValue('trainingData/dz_genre.csv', 'id', genreId)
                        if (genreEntry):
                            ## getCSVRowsByFieldValue() returns a list of lists, but we know only 1 genre per release is possible
                            genre = genreEntry[0][2]
                            if (genre not in genres):
                                genres.append(genre)
                    if(genres):
                        artistData = self.artists[gid]
                        artistData['genres'] = genres
                        self.artists[gid] = artistData
                
    # get top-5 countries by fan count in Twitter
    def addArtistCountriesByFans(self):
        for dataEntry in fileIO.readCSVFile('trainingData/mm_artist_tw_country.csv'):
            gid = dataEntry[1]
            if (gid in self.artists):
                jsonCountries = json.loads(dataEntry[2])
                countries = []
                for countryEntry in jsonCountries[:5]:
                    if (countryEntry['country_code']):
                        countries.append(countryEntry['country_code'])
                artistData = self.artists[gid]
                artistData['fanCountries'] = countries
                self.artists[gid] = artistData   
                
    # get top-5 cities by fan count in Twitter
    def addArtistCitiesByFans(self):
        for dataEntry in fileIO.readCSVFile('trainingData/mm_artist_tw_city.csv'):
            gid = dataEntry[1]
            if (gid in self.artists):
                jsonCities = json.loads(dataEntry[2])
                cities = []
                for cityEntry in jsonCities[:5]:
                    if (cityEntry['city_name']):
                        cities.append(cityEntry['city_name'])
                artistData = self.artists[gid]
                artistData['fanCities'] = cities
                self.artists[gid] = artistData
                
    # get the gender of fans if either males or females are dominant (>66 percent)
    def addArtistFanGender(self):
        for dataEntry in fileIO.readCSVFile('trainingData/mm_artist_demographics_gender.csv'):
            gid = dataEntry[1]
            if (gid in self.artists):
                male = dataEntry[2]
                female = dataEntry[3]
                ratio = float(male) / float(female)
                if (ratio > 2.0):
                    artistData = self.artists[gid]
                    artistData['fanGender'] = 'male'
                    self.artists[gid] = artistData
                elif (ratio < 0.5):
                    artistData = self.artists[gid]
                    artistData['fanGender'] = 'female'
                    self.artists[gid] = artistData
                    
    # get the age of fans if that age group is >6 percent of listeners
    def addArtistFanAge(self):
        for dataEntry in fileIO.readCSVFile('trainingData/mm_artist_demographics_age.csv'):
            gid = dataEntry[1]
            if (gid in self.artists):
                jsonAges = json.loads(dataEntry[2])
                ages = []
                for ageEntry in jsonAges['response']['data']:
                    if (float(ageEntry['percent']) > 6.0):
                        ages.append(ageEntry['age'])
                if (ages):
                    artistData = self.artists[gid]
                    artistData['fanAge'] = ages
                    self.artists[gid] = artistData
    
    # get the IDs of of users who favorited the artists (from Deezer dataset) 
    def addArtistFans(self):
        for dataEntry in fileIO.readCSVFile('trainingData/dz_artist.csv'):
            dz_id = dataEntry[0]
            gid = dataEntry[2]
            if (gid in self.artists):
                fans = fileIO.getCSVRowsByFieldValue('trainingData/dz_artist_fan.csv', 'dz_artist_id', dz_id)
                if (fans):
                    fanIds = []
                    for fanEntry in fans:
                        fanIds.append(fanEntry[1]+"_dz")
                    artistData = self.artists[gid]
                    artistData['fans'] = fanIds
                    self.artists[gid] = artistData
    
    # compute the similarity of two artists using intermediate similarities:
    # tagSimilarity, artistsMatch, genreSimilarity, countrySimilarity,
    # citySimilarity, fanGenderMatch, fanAgeSimilarity, fanCoocurrence, finalSimilarity
    def computeArtistSimilarity(self,gid1,gid2):
        
        similarities = {}
        artistInfo1 = self.artists[gid1]
        artistInfo2 = self.artists[gid2]
        finalSimilarity = 0.0
        
        if (('lfTags' in artistInfo1) and ('lfTags' in artistInfo2)):
            sim = Artists.jaccard(artistInfo1['lfTags'], artistInfo2['lfTags'])
            if (sim > 0):
                similarities['tagSimilarity'] = sim
                finalSimilarity += sim
        
        if (('lfSimilar' in artistInfo1) and ('lfSimilar' in artistInfo2)):
            if (len(set(artistInfo1['lfSimilar']).intersection(artistInfo2['lfSimilar'])) > 0):
                similarities['artistsMatch'] = 1
                finalSimilarity += 1
        
        if (('genres' in artistInfo1) and ('genres' in artistInfo2)):
            sim = Artists.jaccard(artistInfo1['genres'], artistInfo2['genres'])
            if (sim > 0):
                similarities['genreSimilarity'] = sim
                finalSimilarity += sim
        
        if (('fanCountries' in artistInfo1) and ('fanCountries' in artistInfo2)):
            sim = Artists.jaccard(artistInfo1['fanCountries'], artistInfo2['fanCountries'])
            if (sim > 0):
                similarities['countrySimilarity'] = sim
                finalSimilarity += sim
        
        if (('fanCities' in artistInfo1) and ('fanCities' in artistInfo2)):
            sim = Artists.jaccard(artistInfo1['fanCities'], artistInfo2['fanCities'])
            if (sim > 0):
                similarities['citySimilarity'] = sim
                finalSimilarity += sim
        
        if (('fanGender' in artistInfo1) and ('fanGender' in artistInfo2)):
            if (artistInfo1['fanGender'] == artistInfo2['fanGender']):
                similarities['fanGenderMatch'] = 1
                finalSimilarity += 1
        
        if (('fanAge' in artistInfo1) and ('fanAge' in artistInfo2)):
            sim = Artists.jaccard(artistInfo1['fanAge'], artistInfo2['fanAge'])
            if (sim > 0):
                similarities['fanAgeSimilarity'] = sim
                finalSimilarity += sim
        
        if (('fans' in artistInfo1) and ('fans' in artistInfo2)):
            sim = Artists.jaccard(artistInfo1['fans'], artistInfo2['fans'])
            if (sim > 0):
                similarities['fanCoocurrence'] = sim
                finalSimilarity += sim
        
        if (finalSimilarity > 0):
            similarities['finalSimilarity'] = finalSimilarity
        
        return similarities
    
    # compute Jaccard similarity
    @staticmethod
    def jaccard(a, b):
        c = set(a).intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))
    
    # print formatted artist info
    @staticmethod
    def printArtistInfo(artistEntry):
        output = ''
        infoDict = json.loads(artistEntry[1])
        for key in sorted(infoDict.iterkeys()):
            if (key == 'artistName'):
                output = '-' + infoDict[key] + '-\n'
            elif (key == 'fanGender'):
                output += '\t' + key + ': ' + infoDict[key] + '\n'
            elif (key != 'fans'):
                output += '\t' + key + ': ' + ", ".join([str(i) for i in infoDict[key]]) + '\n'
        print output + '-----'
        
        