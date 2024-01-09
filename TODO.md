## Tip: Install TODO Tree extension


## Kriittiset:

### Elias Ervelä:
1. salasanalla kryptatut database tiedostot (missä source filet ja database jsonit)
2. menunäyttöön ajankohtaiset tiedot, mm. käytetty database-tiedoston nimi ja pvm?
3. turnauksen aloittaminen tekee ja avaa nimien inputtaamista varten txt-tiedoston (jota ei gittiin)

### Santeri Salomaa:
1. ~~sh tiedosto, mistä aukeaa UI, ja joka kysyy salasanaa~~
2. ~~file explorer uuden source csv:n inputtaamiseen~~
3. ~~start_tournament metodin siirtäminen ja siistiminen~~
4. käyttöohjeet gitin README-tiedostoon


## Ei kriittiset:

- GUI menulle, missä terminaalinäyttö toisessa ikkunassa


## Old ideas:

- Document and comment e.g. rest of main.py, player.py and game.py files
- Do edit player info (that changes also the games) to main()
- Check if it's to better to save Player instances to json instead of their names in the games database
- Do backups for the databases
- Website frontend (@Lama business)
- Rename variables with capital letter first names when objects (dibs, t. Elias Erv)
- After inputing tournament games, the Leaderboards has the most resent TYLO change. (eg. if you gain 5 TYLO points in a tournament, the leaderboards has +5 there until next games are inputted)
  - It could check all the players who has elo history change the same time as the most resent inputted file and have those players in the list have (+5) in the leaderboard list.
- improve TYLO history plot (grids, y-axis from 0 to n)
- plot TYLO history for multiple players in the same plot
