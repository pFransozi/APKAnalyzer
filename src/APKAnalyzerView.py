from tabulate import tabulate

class APKAnalyzerView():
    
    def show_result(self, apks):

        table_data = []
        headers = ['SEQ.','APK HASH', 'STATUS', 'VIRUSTOTAL LINK']
        seq = 0

        for hash_apk in apks:

            seq = seq + 1

            predict = apks[hash_apk]["prediction"]["total"]

            if predict == 1:
                status = "\033[91mmalware\033[0m"  # Red color for 'malware'
            elif predict == 0:
                status = "goodware"
            else:
                status = "erro"

            url = f"https://www.virustotal.com/gui/file/{hash_apk}"
            link = f"\033]8;;{url}\aVT\033]8;;\a"  # Shortened link text to 'VT'

            table_data.append([seq, hash_apk, status, link])

        print(tabulate(table_data, headers, tablefmt='simple'))