'''
Created on 22.07.2013
@author: Marius Kaminskas
'''

import csv
from artists import Artists

if __name__ == '__main__':
    
    artistData = Artists()
    
    artistData.addArtistNames()
    artistData.addArtistLastFmTags()
    artistData.addArtistCountriesByFans()
    artistData.addArtistCitiesByFans()
    artistData.addArtistFanGender()
    artistData.addArtistFanAge()
    artistData.addArtistGenres()
    artistData.addArtistFans()
    artistData.addSimilarArtists()
    
    # write artist dataset to file
    artistData.printToFile()
    
    # write similar artists to file
    with open('outputData/artist_matrix.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['gid1','gid2','similarity'])
         
        # get top-10 artists for every artist in the dataset
        for artistId1 in artistData.artists:
            results = []
            for artistId2 in artistData.artists:
                if (artistId1 != artistId2):
                    # 'similarities' contains also intermediate similarity values, but we only care about finalSimilarity
                    similarities = artistData.computeArtistSimilarity(artistId1, artistId2)
                    if ('finalSimilarity' in similarities):
                        result = [artistId1, artistId2, similarities['finalSimilarity']]
                        results.append(result)
            # sort results by the similarity, i.e., the third list element
            # then write top-10 results
            for row in sorted(results, key=lambda x: x[2], reverse=True)[:10]:
                writer.writerow(row)
        