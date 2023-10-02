# Konfiguracja Debian Preseed

## Wprowadzenie

Ten projekt zawiera przykładową konfigurację pliku preseed do automatycznego instalowania systemu Debian. Debian Preseed to narzędzie, które umożliwia automatyczną instalację systemu Debian bez interakcji z użytkownikiem. Możesz dostosować ten plik preseed.cfg do własnych potrzeb, aby stworzyć spersonalizowaną konfigurację instalacji systemu Debian.

## Wymagania

1. Obraz instalacyjny systemu Debian (CD, DVD, lub netinst)
2. Dostęp do edycji pliku preseed.cfg w celu dostosowania konfiguracji

Instrukcje użycia

 - Skopiuj skrypty oraz obraz instalacyjny systemu Debian (zalecana wersja netinst).
 - Przygotuj plik preseed.cfg na podstawie przykładu dostępnego w tym projekcie lub dostosuj go do własnych potrzeb. Do wygenerowania hashy użyj skryptu mkpasswd.py
 - Pamiętaj, że plik preseed zawiera szczegółowe instrukcje dotyczące instalacji, takie jak partycjonowanie, wybór paczek i konfigurację sieci.
 - Uruchom skrypt make-preseed-iso.sh on zmodyfikuje obraz płyty i wgra plik preseed.cfg
 - Nagraj obraz na płyte CD lub pendrive i uruchom instalację systemu Debian


## Dostosowywanie pliku preseed.cfg

Plik preseed można dostosować do swoich potrzeb, korzystając z dołączonego konfiguratora, konfigurator ten obsługuję podstawowe pytania pojawiające się podczas procesu instalacji (pominięto konfigurację WiFi), dla skorzystania z dodatkowych opcji odsyłam do dokumentacji. Dokumentacja systemu Debian zawiera szczegółowe informacje na temat dostępnych opcji i ich składni.

Więcej informacji można znaleźć w oficjalnej dokumentacji Debian: Debian Preseeding Wsparcie

