#!/bin/sh -x

# create database with name as dish_test
DATABASE_NAME='dish_test'
if psql -lqt | cut -d \| -f 1 | grep -qw $DATABASE_NAME; then
    echo "A database with the name $DBNAME already exists."
    echo "Drop $DATABASE_NAME and create a new one."
    dropdb $DATABASE_NAME
fi
createdb $DATABASE_NAME

# Export the environment variables and set up for the server
export DATABASE_URL='postgresql://localhost:5432/dish_test' 
export ADMIN_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NDg2NDVjNmRiYzkwZDNkZTJkMDdjIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkyNjAzODEwLCJleHAiOjE1OTI2OTAyMTAsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTpkaXNoZXMiLCJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6ZGlzaGVzIiwicGF0Y2g6cmVzdGF1cmFudHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRpc2hlcyIsInBvc3Q6cmVzdGF1cmFudHMiXX0.ft2me_AL3-ByK2l0wK2PrHbD7Ml8T7Jc-gKsu9tOhyDcB5EqqNbGRdgT_phgZ2dTeD0NUvndbsa7UJdFFDJ_JkvCA7dntQeXgw5tZ-OfBPiI5q0E5dij78D1zd6h9ysRSVvc9qwaENCwovFmWE_OvKIsP0Bqeb2RSiLrATVupFa_JSY8tNP2m9fCKtTFP-C0l5iJa6VU_kC-NpRHrOjBr8peXJ0zPqqiNyzDHdn8nDNkCNuF3a3jV_GMbrr5Ek8OVtzuHBO4wJEG-n1905vlhHbrHbNER2Lmw8Lwzka8zi2QMRGcIbjdYKcj0xfoMLKpVtcu-s2-LBNbxTQ93jG4NA'
export USER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5NTVhN2MzNDdlYjAwYzE3MThhM2MzIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkyNTM2OTI3LCJleHAiOjE1OTI2MjMzMjcsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiXX0.nwToR8EE5_TvHhoVmuBlaGT_cXYX1z0yLIMo8dzCUifASYlxsnxklY_SY0U3ZVrWrNiTY1Hp4alZNsyRUkcVQbwWhaPoalbwWRddzk0vScKoe4b3bB9S-jFVsa3Bt-sEjTKQlEKNk196LPvBd9sG9bcnMkHOpwxElByWiusIUn1OtAL6Bi9Vrjm5itcl265Muk65Ur6Q0IhLtKhyjN9yM8wUfUAIvAUzNtAR35TOT_zDlaAsoH_2w9GQxOflZmK74xg-U2EiZkhGM3svFXmAexwT2KCB4-8LEZ4n640s2rRuDNxvamaRCxtOLPtONNda8pEacccLXzZURI47R9NNCA' 
python3 -m backend.src.test -v