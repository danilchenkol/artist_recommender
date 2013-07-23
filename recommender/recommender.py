'''
Created on 22.07.2013
@author: Marius Kaminskas
'''

import fileIO, artists

if __name__ == '__main__':
    
    while True:
        artistName = raw_input("Enter artist name: ")
        if len(artistName) > 0:
            foundId = fileIO.getArtistByName(artistName)
            if (foundId):
                print "Found artist:"
                artistInfo = fileIO.getCSVRowsByFieldValue('outputData/artist_info.csv', 'gid', foundId)[0]
                artists.Artists.printArtistInfo(artistInfo)
                print "Similar artists:\n---------------"
                
                similarArtists = fileIO.getCSVRowsByFieldValue('outputData/artist_matrix.csv', 'gid1', foundId)
                if (similarArtists):
                    for row in similarArtists:
                        similarArtist = row[1]
                        similarArtistInfo = fileIO.getCSVRowsByFieldValue('outputData/artist_info.csv', 'gid', similarArtist)[0]
                        artists.Artists.printArtistInfo(similarArtistInfo)
                else:
                    print 'No similar artists could be found in the dataset. Insufficient information about the artist.'
                
                searchAgain = raw_input("Search for another artist? (Y/N)")
                answer = searchAgain.upper()
                if (answer != 'Y'):
                    break
            else:
                print 'The entered artist not found in the dataset. Try again.'
    
    
    
    
    
    